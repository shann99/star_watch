from datetime import date, datetime, timezone

import requests
from flask import Flask, g
from flask_apscheduler import APScheduler
from flask_login import current_user, login_user
from lxml import html
from sqlalchemy import func

from star_watch import app, db
from star_watch.models import Card, Tags, User

scheduler = APScheduler()


@scheduler.task("cron", hour=9, minute=15)
def dateChecker():
    with app.app_context():
        # user=current_user
        # print(user)

        user = User.query.first()

        today = date.today()

        ended_list = (
            Card.query.with_entities(Card.release_ended, Card.id)
            .filter(Card.release_status == "Currently Releasing")
            .join(User)
            .filter(User.id == user.id)
            .all()
        )

        ended = dict([(key, value) for key, value in ended_list])
        ended_dict = {
            key: value for key, value in ended.items() if key != None and key != ""
        }

        for key, value in ended_dict.items():
            if key != None or key != "":
                if key.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
                    card = db.session.get(Card, value)
                    card.release_status = "Released"
                    db.session.commit()

        update_list = (
            Card.query.with_entities(Card.release_date, Card.id)
            .filter(Card.release_status == "Scheduled Release")
            .join(User)
            .filter(User.id == user.id)
            .all()
        )

        update = dict([(key, value) for key, value in update_list])
        update_dict = {key: value for key, value in update.items()}

        for key, value in update_dict.items():
            if key != None or key != "":
                if key.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
                    card = db.session.get(Card, value)
                    if card.media_type == "Anime":
                        try:
                            anilist_id = int(card.anilistId)
                            anilist_query = """
                                query ($id: Int) { # Define which variables will be used in the query (id)
                                    Media(id: $id, type: ANIME, genre_not_in: "Hentai", format_not: MUSIC) {
                                        description(asHtml: false)
                                        episodes
                                        coverImage {
                                            extraLarge
                                            large
                                            medium
                                            color
                                        }
                                        endDate {
                                            year
                                            month
                                            day
                                            }
                                    }
                                }
                                """
                            variables = {"id": anilist_id}
                            anilist_url = "https://graphql.anilist.co"
                            anilist_response = requests.post(
                                anilist_url,
                                json={"query": anilist_query, "variables": variables},
                            )
                            anilist_returned = anilist_response.json()
                            if (
                                anilist_returned["data"]["Media"]["description"] != None
                                and anilist_returned["data"]["Media"]["description"]
                                != ""
                            ):
                                card.description = html.fromstring(
                                    anilist_returned["data"]["Media"]["description"]
                                ).text_content()
                            else:
                                card.description = "No description available"
                            card.total_eps = anilist_returned["data"]["Media"][
                                "episodes"
                            ]
                            card.image = anilist_returned["data"]["Media"][
                                "coverImage"
                            ]["extraLarge"]
                            if (
                                anilist_returned["data"]["Media"]["endDate"]["month"]
                                != None
                            ):
                                endDate = f"{anilist_returned['data']['Media']['endDate']['month']}-{anilist_returned['data']['Media']['endDate']['day']}-{anilist_returned['data']['Media']['endDate']['year']}"
                                card.release_ended = datetime.strptime(
                                    endDate, "%m-%d-%Y"
                                ).date()
                            elif (
                                anilist_returned["data"]["Media"]["endDate"]["month"]
                                != None
                                and anilist_returned["data"]["Media"]["endDate"]["day"]
                                == None
                                and anilist_returned["data"]["Media"]["endDate"]["year"]
                                != None
                            ):
                                endDate = f"{anilist_returned['data']['Media']['endDate']['month']}-{anilist_returned['data']['Media']['endDate']['year']}"
                                card.release_ended = datetime.strptime(
                                    endDate, "%m-%Y"
                                ).date()
                            else:
                                card.release_ended = None
                            card.release_status = "Currently Releasing"

                            db.session.commit()
                        except:
                            print("Error. Cannot find anilist id")
                            print(card.anilistId)
                        else:
                            print("Something went super wrong")
                            print(card.anilistId)
                    elif card.media_type == "Movie":
                        card.release_status = "Released"
                        db.session.commit()
                    else:
                        try:
                            tvmaze_id = card.tvmazeId
                            tvmaze_url = f"https://api.tvmaze.com/shows/{tvmaze_id}?embed=episodes"
                            tvmaze_response = requests.get(tvmaze_url)
                            tvmaze_returned = tvmaze_response.json()
                            if tvmaze_returned["summary"] != None:
                                card.description = html.fromstring(
                                    tvmaze_returned["summary"]
                                ).text_content()
                            else:
                                card.description = "No description available"
                            if tvmaze_returned["ended"] != None:
                                card.release_ended = datetime.strptime(
                                    tvmaze_returned["ended"], "%Y-%m-%d"
                                ).date()
                            else:
                                card.release_ended = None
                            if tvmaze_returned["schedule"]["days"] != None:
                                card.release_weekly = tvmaze_returned["schedule"][
                                    "days"
                                ][0]
                            else:
                                card.release_weekly = ""
                            card.total_eps = len(
                                tvmaze_returned["_embedded"]["episodes"]
                            )
                            card.release_status = "Currently Releasing"
                            db.session.commit()
                        except:
                            print("Error with tvmazeid")
                            print(card.tvmazeId)
                        else:
                            print("something really went wrong")
                            print(card.tvmazeId)

        weekly_releasing = []

        weekly = (
            Card.query.with_entities(Card.release_weekly, Card.release_status)
            .join(User)
            .filter(User.id == user.id)
            .all()
        )

        item_dict = dict([(key, value) for key, value in weekly])
        item_dict = {
            key: value
            for key, value in item_dict.items()
            if value != "Scheduled Release"
        }

        for key, value in item_dict.items():
            if key != None and key != "":
                weekly_releasing.append(key)

        counter = 0

        for releasing in weekly_releasing:
            if releasing == today.strftime("%A"):
                counter += 1

        user.alert = counter

        db.session.commit()


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
