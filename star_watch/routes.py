import json
import os
import random
import time
from datetime import date, datetime, timezone
from io import StringIO
from pprint import pprint as pp

import numpy as np
import requests
from flask import (
    flash,
    get_flashed_messages,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from lxml import html
from sqlalchemy import func, or_
from werkzeug.security import check_password_hash, generate_password_hash

from main import dateChecker
from star_watch import app, db
from star_watch.models import Card, Tags, User


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = current_user
    # querying images where watch status equals watching
    item_list = (
        Card.query.with_entities(Card.image, Card.title)
        .filter(Card.status == "Watching")
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    # retrieving the image itself without the extra parenthesis and commas from the query list
    item_dict = dict([(key, value) for key, value in item_list])
    item_dict = {
        key: value for key, value in item_dict.items() if key != "/background.jpg"
    }
    dict_list = list(item_dict.items())
    np.random.shuffle(dict_list)
    shuffled_dict = dict(dict_list)

    images = []
    titles = []
    for key, value in shuffled_dict.items():
        images.append(key)
        titles.append(value)

    page = request.args.get("page", 1, type=int)

    card_ids = []
    for item in titles:
        cardId = (
            Card.query.with_entities(Card.title, Card.id)
            .filter(Card.title == item)
            .join(User)
            .filter(User.id == user.id)
            .first()
        )
        card_ids.append(cardId)
    # print(card_ids)
    cards_dict = dict([(key, value) for key, value in card_ids])

    id_list = []
    for key, value in cards_dict.items():
        id_list.append(value)
    print(id_list)

    watching_list = (
        Card.query.filter(Card.status == "Watching")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.release_status)
        .order_by(Card.title.asc())
        .paginate(page=page, per_page=15)
    )

    prev_page = url_for("index", page=watching_list.prev_num)
    next_page = url_for("index", page=watching_list.next_num)
    total_pgs = watching_list.pages
    if next_page == "/index":
        next_page = total_pgs

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "index.html",
        user=current_user,
        cards=watching_list,
        today=today,
        currentRel=currentRelease_list,
        scheduled=scheduledRelease_list,
        releases_dates=releases_dates,
        images=images,
        titles=titles,
        ids=id_list,
        next_page=next_page,
        prev_page=prev_page,
        total_pgs=total_pgs,
        page=page,
    )


@app.route("/planning", methods=["GET", "POST"])
@login_required
def planning():
    user = current_user
    page = request.args.get("page", 1, type=int)

    planning_list = (
        Card.query.filter(Card.status == "Planning")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.date_edited.desc())
        .paginate(page=page, per_page=20)
    )

    prev_page = url_for("planning", page=planning_list.prev_num)
    next_page = url_for("planning", page=planning_list.next_num)
    total_pgs = planning_list.pages
    if next_page == "/planning":
        next_page = total_pgs

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "planning.html",
        user=current_user,
        cards=planning_list,
        today=today,
        currentRel=currentRelease_list,
        scheduled=scheduledRelease_list,
        releases_dates=releases_dates,
        next_page=next_page,
        prev_page=prev_page,
        total_pgs=total_pgs,
        page=page,
    )


@app.route("/paused", methods=["GET", "POST"])
@login_required
def paused():
    user = current_user
    page = request.args.get("page", 1, type=int)
    paused_list = (
        Card.query.filter(Card.status == "Paused")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.date_edited.desc())
        .paginate(page=page, per_page=20)
    )

    prev_page = url_for("paused", page=paused_list.prev_num)
    next_page = url_for("paused", page=paused_list.next_num)
    total_pgs = paused_list.pages
    if next_page == "/paused":
        next_page = total_pgs

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "paused.html",
        user=current_user,
        cards=paused_list,
        today=today,
        currentRel=currentRelease_list,
        scheduled=scheduledRelease_list,
        releases_dates=releases_dates,
        next_page=next_page,
        prev_page=prev_page,
        total_pgs=total_pgs,
        page=page,
    )


@app.route("/completed", methods=["GET", "POST"])
@login_required
def completed():
    user = current_user

    page = request.args.get("page", 1, type=int)
    completed_list = (
        Card.query.filter(Card.status == "Completed")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.date_edited.desc())
        .paginate(page=page, per_page=20)
    )

    prev_page = url_for("completed", page=completed_list.prev_num)
    next_page = url_for("completed", page=completed_list.next_num)
    total_pgs = completed_list.pages
    if next_page == "/completed":
        next_page = total_pgs

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "completed.html",
        user=current_user,
        scheduled=scheduledRelease_list,
        cards=completed_list,
        currentRel=currentRelease_list,
        today=today,
        releases_dates=releases_dates,
        next_page=next_page,
        prev_page=prev_page,
        total_pgs=total_pgs,
        page=page,
    )


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user = current_user
    if request.method == "POST":
        update_user = User.query.get(user.id)

        password = request.form.get("update_password")
        pass_confirm = request.form.get("update_password_confirm")

        if password != pass_confirm:
            flash("Passwords must match, please try again", category="error")
        else:
            if request.form.get("update_profile_pic") != "":
                update_user.profile_pic = request.form.get("update_profile_pic")
            if request.form.get("update_email") != "":
                update_user.email = request.form.get("update_email")
            if request.form.get("update_name") != "":
                update_user.name = request.form.get("update_name")
            if request.form.get("update_password") != "":
                password = generate_password_hash(password, method="sha256")
                update_user.password = password
            db.session.commit()

            success_message = "Your account has successfully been updated!"
            flash(success_message, category="success")
            return redirect(url_for("index"))

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "settings.html",
        user=current_user,
        scheduled=scheduledRelease_list,
        releases_dates=releases_dates,
        today=today,
        currentRel=currentRelease_list,
    )


@app.route("/statistics", methods=["GET", "POST"])
@login_required
def stats():
    user = current_user
    # list counts
    watching_count = (
        Card.query.filter(Card.status == "Watching")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )
    planning_count = (
        Card.query.filter(Card.status == "Planning")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )
    paused_count = (
        Card.query.filter(Card.status == "Paused")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )
    completed_count = (
        Card.query.filter(Card.status == "Completed")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )

    # language count
    language_count = (
        Card.query.with_entities(Card.language, func.count(Card.language))
        .join(User)
        .filter(User.id == user.id)
        .group_by(Card.language)
        .all()
    )
    languages = [lang[0] for lang in language_count]
    nums = [num[1] for num in language_count]

    # media count
    media_count = (
        Card.query.with_entities(Card.media_type, func.count(Card.media_type))
        .join(User)
        .filter(User.id == user.id)
        .group_by(Card.media_type)
        .all()
    )
    type = [med[0] for med in media_count]
    amt = [num[1] for num in media_count]

    # tags count
    tag_count = (
        Tags.query.with_entities(Tags.name, func.count(Tags.name))
        .join(Card, Tags.card_id == Card.id)
        .join(User)
        .filter(Card.user_id == user.id)
        .group_by(Tags.name)
        .order_by(func.count(Tags.name).desc())
        .limit(15)
    )
    tag_name = [tagname[0] for tagname in tag_count]
    tag_num = [tagnum[1] for tagnum in tag_count]

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())

    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "stats.html",
        user=current_user,
        today=today,
        currentRel=currentRelease_list,
        scheduled=scheduledRelease_list,
        releases_dates=releases_dates,
        langs=languages,
        nums=nums,
        tag_name=tag_name,
        tag_num=tag_num,
        type=type,
        amt=amt,
        watch_count=watching_count,
        plan_count=planning_count,
        pause_count=paused_count,
        complete_count=completed_count,
    )


@app.route("/favorites", methods=["GET", "POST"])
@login_required
def favorites():
    user = current_user
    favorites_count = (
        Card.query.filter(Card.fav == True)
        .join(User)
        .filter(User.id == user.id)
        .count()
    )
    # favorites
    page = request.args.get("page", 1, type=int)

    favorites_list = (
        Card.query.filter(Card.fav == True)
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
        .paginate(page=page, per_page=15)
    )

    prev_page = url_for("favorites", page=favorites_list.prev_num)
    next_page = url_for("favorites", page=favorites_list.next_num)
    total_pgs = favorites_list.pages
    if next_page == "/favorites":
        next_page = total_pgs

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )

    return render_template(
        "favorites.html",
        today=today,
        releases_dates=releases_dates,
        currentRel=currentRelease_list,
        scheduled=scheduledRelease_list,
        user=current_user,
        cards=favorites_list,
        next_page=next_page,
        prev_page=prev_page,
        total_pgs=total_pgs,
        page=page,
        fav_count=favorites_count,
    )


@app.route("/releases", methods=["GET", "POST"])
@login_required
def releases():
    user = current_user
    releases = (
        Card.query.filter(Card.release_status != "Released")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )
    # releases pagination
    page = request.args.get("page", 1, type=int)

    super_releases = (
        Card.query.filter(Card.release_status != "Released")
        .join(User)
        .filter(User.id == user.id)
        .paginate(page=page, per_page=100)
    )

    unreleased_list = (
        Card.query.filter(Card.release_status == "Not yet released")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    unreleased_count = (
        Card.query.filter(Card.release_status == "Not yet released")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )

    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.release_information.asc())
    )
    scheduledRelease_count = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )

    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    currentRelease_count = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .count()
    )

    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()

    weekdays = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    weekly_releasing = []
    for item in dates:
        for weekday in weekdays:
            if item != None and item != "" and weekday in item:
                weekly_releasing.append(weekday)

    return render_template(
        "releases.html",
        today=today,
        user=current_user,
        cards=super_releases,
        unreleased=unreleased_list,
        releases_dates=releases_dates,
        scheduled=scheduledRelease_list,
        currentRel=currentRelease_list,
        releases=releases,
        unrelcount=unreleased_count,
        schedcount=scheduledRelease_count,
        currentcount=currentRelease_count,
    )


@app.route("/alerts", methods=["POST"])
@login_required
def alerts():
    curr_user = User.query.get(request.form["user_id"])
    curr_user.alert = 0
    db.session.commit()
    return "", 204


@app.route("/delete_tag", methods=["POST"])
@login_required
def delete_tag():
    if request.method == "POST":
        tag = request.form["tag_id"]
        del_tag = Tags.query.get(tag)
        db.session.delete(del_tag)
        db.session.commit()
        return "", 204


@app.route("/update_tag", methods=["POST"])
@login_required
def update_tag():
    if request.method == "POST":
        update_tagID = request.form["tag_id"]
        tag = Tags.query.get(update_tagID)
        tag_name = request.form["tag_update"]
        if request.form["tag_update"] != None:
            tag.name = request.form["tag_update"]
        db.session.commit()
        return "", 204


# add media manually
@app.route("/add_media", methods=["POST"])
@login_required
def add_media():
    user = current_user
    if request.method == "POST":
        if request.form.get("add_image_form") != "":
            image = request.form.get("add_image_form")
        else:
            image = url_for("static", filename="background.jpg")
        title = request.form.get("add_title")
        if request.form.get("current_ep") != "":
            current_ep = request.form.get("current_ep")
        else:
            current_ep = 0
        if request.form.get("total_eps") != "":
            total_eps = request.form.get("total_eps")
        else:
            total_eps = "?"
        if request.form.get("type") != "":
            media_type = request.form.get("type")
        else:
            media_type = "unknown"
        if request.form.get("language") != "":
            language = request.form.get("language")
        else:
            language = "unknown"
        if (
            request.form.get("release_status") != ""
            or request.form.get("release_status") != "Select Release Status"
        ):
            release_status = request.form.get("release_status")
        else:
            release_status = "Released"
        if request.form.get("release_information") != "":
            release_information = request.form.get("release_information")

        else:
            release_information = ""
        description = request.form.get("description")
        rating = request.form.get("rating")
        status = request.form.get("status")
        fav = False

        card = Card(
            title=title,
            image=image,
            current_ep=current_ep,
            total_eps=total_eps,
            status=status,
            description=description,
            rating=rating,
            fav=fav,
            release_status=release_status,
            release_information=release_information,
            media_type=media_type,
            language=language,
            user=current_user,
        )

        db.session.add(card)
        db.session.commit()

        weekdays = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        today = date.today()

        if (
            request.form.get("release_information") != ""
            and request.form.get("release_information").startswith("Weekly") is False
        ):
            date_obj = datetime.strptime(
                request.form.get("release_information"), "%Y-%m-%d"
            )
            if date_obj.date() == today:
                dateChecker()

        if request.form.get("release_information") != "" and request.form.get(
            "release_information"
        ).startswith("Weekly"):
            for weekday in weekdays:
                if weekday in request.form.get(
                    "release_information"
                ) and weekday == today.strftime("%A"):
                    dateChecker()

        flash("Your new media has sucessfully been added!", category="success")
        return redirect(request.referrer)


# add media from search
@app.route("/add-from-search", methods=["POST"])
@login_required
def add_from_search():
    user = current_user
    if request.method == "POST":
        source = request.form.get("sourceFrom")
        if source == "anilist":
            anilist_id = int(request.form.get("apiId"))
            anilist_query = """
            query ($id: Int) { # Define which variables will be used in the query (id)
            Media(id: $id, type: ANIME, genre_not_in: "Hentai", format_not: MUSIC) {
                title {
                    romaji
                    english
                    native
                }
                description(asHtml: false)
                episodes
                coverImage {
                    extraLarge
                    large
                    medium
                    color
                }
                bannerImage
                genres
                status
                countryOfOrigin
                id
                seasonYear
                endDate {
                    year
                    month
                    day
                }
                startDate {
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
                anilist_url, json={"query": anilist_query, "variables": variables}
            )
            anilist_returned = anilist_response.json()
            romajiTitle = anilist_returned["data"]["Media"]["title"]["romaji"]
            if anilist_returned["data"]["Media"]["title"]["english"] != None:
                engTitle = anilist_returned["data"]["Media"]["title"]["english"]
            else:
                engTitle = romajiTitle
            if (
                anilist_returned["data"]["Media"]["description"] != None
                and anilist_returned["data"]["Media"]["description"] != ""
            ):
                description = html.fromstring(
                    anilist_returned["data"]["Media"]["description"]
                ).text_content()
            else:
                description = "No description available"
            totalEps = anilist_returned["data"]["Media"]["episodes"]
            if anilist_returned["data"]["Media"]["bannerImage"] != None:
                image = anilist_returned["data"]["Media"]["bannerImage"]
            else:
                image = anilist_returned["data"]["Media"]["coverImage"]["extraLarge"]
            if (
                anilist_returned["data"]["Media"]["startDate"]["month"] != None
                and anilist_returned["data"]["Media"]["startDate"]["day"] != None
                and anilist_returned["data"]["Media"]["startDate"]["year"] != None
            ):
                startDate = f"{anilist_returned['data']['Media']['startDate']['month']}-{anilist_returned['data']['Media']['startDate']['day']}-{anilist_returned['data']['Media']['startDate']['year']}"
                start_date_object = datetime.strptime(startDate, "%m-%d-%Y").date()

            elif (
                anilist_returned["data"]["Media"]["startDate"]["month"] != None
                and anilist_returned["data"]["Media"]["startDate"]["day"] == None
                and anilist_returned["data"]["Media"]["startDate"]["year"] != None
            ):
                startDate = f"{anilist_returned['data']['Media']['startDate']['month']}-{anilist_returned['data']['Media']['startDate']['year']}"
                start_date_object = datetime.strptime(startDate, "%m-%Y").date()
            else:
                start_date_object = None
            if anilist_returned["data"]["Media"]["endDate"]["month"] != None:
                endDate = f"{anilist_returned['data']['Media']['endDate']['month']}-{anilist_returned['data']['Media']['endDate']['day']}-{anilist_returned['data']['Media']['endDate']['year']}"
                end_date_object = datetime.strptime(endDate, "%m-%d-%Y").date()
            elif (
                anilist_returned["data"]["Media"]["endDate"]["month"] != None
                and anilist_returned["data"]["Media"]["endDate"]["day"] == None
                and anilist_returned["data"]["Media"]["endDate"]["year"] != None
            ):
                endDate = f"{anilist_returned['data']['Media']['endDate']['month']}-{anilist_returned['data']['Media']['endDate']['year']}"
                end_date_object = datetime.strptime(endDate, "%m-%Y").date()
            else:
                end_date_object = None
            if anilist_returned["data"]["Media"]["countryOfOrigin"] == "CN":
                language = "Chinese"
                media_type = "Donghua"
            else:
                language = "Japanese"
                media_type = "Anime"
            if anilist_returned["data"]["Media"]["status"] == "RELEASING":
                release_status = "Currently Releasing"
            elif (
                anilist_returned["data"]["Media"]["status"] == "NOT_YET_RELEASED"
                and anilist_returned["data"]["Media"]["startDate"]["month"] == None
            ):
                release_status = "Not yet released"
            elif (
                anilist_returned["data"]["Media"]["status"] == "NOT_YET_RELEASED"
                and anilist_returned["data"]["Media"]["startDate"]["month"] != None
            ):
                release_status = "Scheduled Release"
            else:
                release_status = "Released"
            status = "Planning"
            rating = "?"
            card = Card(
                title=engTitle,
                romajiTitle=romajiTitle,
                image=image,
                current_ep=0,
                total_eps=totalEps,
                status=status,
                description=description,
                rating=rating,
                fav=False,
                release_status=release_status,
                release_date=start_date_object,
                release_ended=end_date_object,
                media_type=media_type,
                language=language,
                anilistId=anilist_id,
                user=current_user,
            )

            db.session.add(card)
            db.session.commit()
            for genre in anilist_returned["data"]["Media"]["genres"]:
                tag = Tags(name=genre.lower(), card_id=card.id)
                db.session.add(tag)
                db.session.commit()

            flash(f"{card.title} was added!", category="success")
            return "", 204

        elif source == "tvmaze":
            tvmaze_id = request.form.get("apiId")
            tvmaze_url = "https://api.tvmaze.com/lookup/shows?thetvdb="
            tvmaze_response = requests.get(tvmaze_url + tvmaze_id)
            tvmaze_returned = tvmaze_response.json()
            title = tvmaze_returned["name"]
            image = tvmaze_returned["image"]["original"]
            if tvmaze_returned["summary"] != None:
                description = html.fromstring(tvmaze_returned["summary"]).text_content()
            else:
                description = "No description available"
            if tvmaze_returned["premiered"] != None:
                start_date = datetime.strptime(
                    tvmaze_returned["premiered"], "%Y-%m-%d"
                ).date()
            else:
                start_date = None
            if tvmaze_returned["ended"] != None:
                end_date = datetime.strptime(
                    tvmaze_returned["ended"], "%Y-%m-%d"
                ).date()
            else:
                end_date = None
            if tvmaze_returned["status"] == "Running":
                release_status = "Currently Releasing"
            elif tvmaze_returned["status"] == "In Development":
                release_status = "Not yet released"
            else:
                release_status = "Released"
            language = tvmaze_returned["language"]
            if language == "Korean" or language == "Japanese":
                media_type = "Drama"
            elif tvmaze_returned["type"] == "Animation":
                media_type = "Animation/Cartoon"
            elif (
                language != "Korean"
                and language != "Japanese"
                and tvmaze_returned["type"] == "Scripted"
            ):
                media_type = "Show"
            else:
                media_type = "other"

            card = Card(
                title=title,
                image=image,
                current_ep=0,
                total_eps="?",
                status="Planning",
                description=description,
                rating="?",
                fav=False,
                release_status=release_status,
                release_date=start_date,
                release_ended=end_date,
                media_type=media_type,
                language=language,
                tvmazeId=tvmaze_id,
                user=current_user,
            )

            db.session.add(card)
            db.session.commit()
            for genre in tvmaze_returned["genres"]:
                tag = Tags(name=genre.lower(), card_id=card.id)
                db.session.add(tag)
                db.session.commit()

            flash(f"{card.title} was added!", category="success")
            return "", 204

        else:
            omdb_id = request.form.get("apiId")
            omdb_key = app.config["OMDB_KEY"]
            omdb_url = "http://www.omdbapi.com/?i="
            omdb_response = requests.get(
                f"{omdb_url}{omdb_id}&plot=short&type=movie&apikey={omdb_key}"
            )
            omdb_returned = omdb_response.json()
            title = omdb_returned["Title"]
            if omdb_returned["Released"] != None:
                release_status = "Released"
                date = omdb_returned["Released"]
                release_date = datetime.strptime(date, "%d %b %Y").date()
            else:
                release_status = "Not yet released"
                release_date = None
            image = omdb_returned["Poster"]
            if omdb_returned["Plot"] != None:
                description = omdb_returned["Plot"]
            else:
                description = "No description available"
            language_list = omdb_returned["Language"].split(",")
            if len(language_list) > 1:
                language = "Multi"
            else:
                language = omdb_returned["Language"]
            media_type = "Movie"
            card = Card(
                title=title,
                image=image,
                current_ep=0,
                total_eps=1,
                status="Planning",
                description=description,
                rating="?",
                fav=False,
                release_status=release_status,
                release_date=release_date,
                media_type=media_type,
                language=language,
                omdbId=omdb_id,
                user=current_user,
            )

            db.session.add(card)
            db.session.commit()

            genres = omdb_returned["Genre"].split(",")
            for genre in genres:
                tag = Tags(name=genre.lower(), card_id=card.id)
                db.session.add(tag)
                db.session.commit()

            flash(f"{card.title} was added!", category="success")
            return "", 204

    return "", 204


# edit card
@app.route("/edit/card/<int:card_id>", methods=["GET", "POST"], strict_slashes=False)
@login_required
def editMedia(card_id):
    card = Card.query.get(card_id)
    if request.method == "POST":
        if request.form.get("edit_image_form") != "":
            card.image = request.form.get("edit_image_form")
        if request.form.get("edit_title") != "":
            card.title = request.form.get("edit_title")
        if request.form.get("edit_current_ep") != "":
            card.current_ep = request.form.get("edit_current_ep")
        if request.form.get("edit_total_eps") != "":
            card.total_eps = request.form.get("edit_total_eps")
        if request.form.get("edit_description") != "":
            card.description = request.form.get("edit_description")
        if request.form.get("edit_rating") != "":
            card.rating = request.form.get("edit_rating")
        if request.form.get("edit_type") != "":
            card.media_type = request.form.get("edit_type")
        if request.form.get("edit_language") != "":
            card.language = request.form.get("edit_language")
        if request.form.get("edit_release_status") != "":
            card.release_status = request.form.get("edit_release_status")
            if request.form.get("edit_release_status") == "Released":
                card.release_information = ""
        if request.form.get("edit_release_information") != "":
            card.release_information = request.form.get("edit_release_information")
        if request.form.get("edit_status") != card.status:
            card.status = request.form.get("edit_status")
            card.date_edited = datetime.now(timezone.utc)
        card.id = card_id
        db.session.commit()

        weekdays = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        today = date.today()

        if (
            request.form.get("edit_release_information") != ""
            and request.form.get("edit_release_information").startswith("Weekly")
            is False
        ):
            date_obj = datetime.strptime(
                request.form.get("edit_release_information"), "%Y-%m-%d"
            )
            if date_obj.date() == today:
                dateChecker()

        if request.form.get("edit_release_information") != "" and request.form.get(
            "edit_release_information"
        ).startswith("Weekly"):
            for weekday in weekdays:
                if weekday in request.form.get(
                    "edit_release_information"
                ) and weekday == today.strftime("%A"):
                    dateChecker()

        flash(f"{card.title} was updated!", category="success")
        return redirect(request.referrer)

    return render_template("edit.html", user=current_user, card_id=card_id)


# delete item
@app.route("/delete/<int:card_id>", methods=["POST"])
@login_required
def delete(card_id):
    user = current_user
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()
    if user.alert != 0:
        dateChecker()
    flash("Your media has been deleted", category="info")
    return redirect(request.referrer)


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            email = request.form.get("login_address")
            password = request.form.get("login_pass")

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", category="success")
                    login_user(user, remember=False)
                    return redirect(url_for("index"))
                else:
                    flash("Incorrect password, please try again", category="error")

            else:
                flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)


# signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            email = request.form.get("email_address")
            name = request.form.get("name")
            password = request.form.get("pass_org")
            pass_confirm = request.form.get("pass_confirm")

            if password != pass_confirm:
                flash("Passwords must match, please try again", category="error")
            else:
                user = User.query.filter_by(email=email).first()
                if user:
                    flash("Email already exists", category="error")

                else:
                    # mode=0 -> default light mode, mode = 1 -> means user has dark mode enabled
                    new_user = User(
                        email=email,
                        name=name,
                        password=generate_password_hash(password, method="sha256"),
                        mode="light",
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    flash("Account successfully created!", category="success")
                    return redirect(url_for("index"))

    return render_template("signup.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", category="success")
    return redirect(url_for("login"))


@app.route("/delete_account/", methods=["POST"])
@login_required
def delete_account():
    if request.method == "POST":
        user = current_user
        delete_user = User.query.get(user.id)

        db.session.delete(delete_user)
        db.session.commit()

        flash("Your account has been deleted", category="success")
        return redirect(url_for("login"))


# <--------misc stuff-------->
@app.route("/fav/", methods=["POST"])
@login_required
def fav():
    if request.method == "POST":
        card = Card.query.get(request.form["card_id"])
        if request.form["card_fav"] == "true":
            card.fav = True
        db.session.commit()
        return "", 204


@app.route("/unfav", methods=["POST"])
@login_required
def unfav():
    if request.method == "POST":
        card = Card.query.get(request.form["card_id"])
        if request.form["card_fav"] == "false":
            card.fav = False
        db.session.commit()
        return "", 204


@app.route("/tag", methods=["POST"])
@login_required
def tags():
    if request.method == "POST":
        card = Card.query.get(request.form["card_id"])
        test_tag = request.form.get("new_tag")
        new_tag = Tags(name=test_tag, card_id=card.id)
        db.session.add(new_tag)
        db.session.commit()

        return "", 204


# updating count with click of a button
@app.route("/upcount", methods=["POST"])
@login_required
def upcount():
    card = Card.query.get(request.form["card_id"])
    card.current_ep += 1
    db.session.commit()
    return "", 204


# search results
@app.route("/search", methods=["GET"])
@login_required
def search():
    user = current_user
    dates_list = (
        Card.query.with_entities(Card.release_information)
        .join(User)
        .filter(User.id == user.id)
        .all()
    )
    dates = [date[0] for date in dates_list]
    releases_dates = []
    for item in dates:
        if item != None and item != "" and item.startswith("Weekly") is False:
            datetime_object = datetime.strptime(item, "%Y-%m-%d")
            releases_dates.append(datetime_object.date())
    today = date.today()
    currentRelease_list = (
        Card.query.filter(Card.release_status == "Currently Releasing")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    scheduledRelease_list = (
        Card.query.filter(Card.release_status == "Scheduled Release")
        .join(User)
        .filter(User.id == user.id)
        .order_by(Card.title.asc())
    )
    if request.method == "GET":
        name = request.args.get("q")
        page = request.args.get("page", 1, type=int)
        search_cards = (
            Card.query.filter(
                or_(Card.title.like(f"%{name}%"), Card.romajiTitle.like(f"%{name}%"))
            )
            .join(User)
            .filter(User.id == user.id)
            .order_by(Card.title.asc())
            .paginate(page=page, per_page=9)
        )
        search_amt = (
            Card.query.filter(
                or_(Card.title.like(f"%{name}%"), Card.romajiTitle.like(f"%{name}%"))
            )
            .join(User)
            .filter(User.id == user.id)
            .order_by(Card.title.asc())
            .all()
        )
        prev_page = search_cards.prev_num
        next_page = search_cards.next_num
        total_pgs = search_cards.pages
        if next_page == "/search":
            next_page = total_pgs
        return render_template(
            "search.html",
            user=current_user,
            cards=search_cards,
            today=today,
            currentRel=currentRelease_list,
            scheduled=scheduledRelease_list,
            releases_dates=releases_dates,
            search_query=name,
            next_page=next_page,
            prev_page=prev_page,
            total_pgs=total_pgs,
            page=page,
            card_amount=search_amt,
        )


@app.route("/dark-mode", methods=["POST"])
@login_required
def dark_mode():
    if request.method == "POST":
        user = User.query.get(request.form["user_id"])
        user.mode = "dark"
        db.session.commit()
        return "", 204


@app.route("/light-mode", methods=["POST"])
@login_required
def light_mode():
    if request.method == "POST":
        user = User.query.get(request.form["user_id"])
        user.mode = "light"
        db.session.commit()
        return "", 204


@app.route("/system-mode", methods=["POST"])
@login_required
def system_mode():
    if request.method == "POST":
        user = User.query.get(request.form["user_id"])
        user.mode = "system"
        db.session.commit()
        return "", 204


@app.route("/change-status", methods=["POST"])
@login_required
def change_status():
    if request.method == "POST":
        update_status = request.form["card_id"]
        card = Card.query.get(update_status)
        card.status = "Completed"
        if card.release_status != "Scheduled Release":
            card.release_status = "Released"
        card.date_edited = datetime.now(timezone.utc)
        db.session.commit()
        flash(f"{card.title} was moved to Completed!", category="success")
        return "", 204
