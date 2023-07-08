from datetime import date, datetime, timezone

from flask import Flask, g
from flask_apscheduler import APScheduler
from flask_login import current_user, login_user
from sqlalchemy import func

from star_watch import app, db
from star_watch.models import Card, Tags, User

scheduler = APScheduler()


@scheduler.task("cron", hour=9, minute=35)
def dateChecker():
    with app.app_context():
        # user=current_user
        # print(user)
        user = User.query.first()
        scheduledRelease_list = (
            Card.query.filter(Card.release_status == "Scheduled Release")
            .join(User)
            .filter(User.id == user.id)
            .order_by(Card.title.asc())
        )
        currentRelease_list = (
            Card.query.filter(Card.release_status == "Currently Releasing")
            .join(User)
            .filter(User.id == user.id)
            .order_by(Card.title.asc())
        )
        dates_list = (
            Card.query.with_entities(Card.release_date)
            .join(User)
            .filter(User.id == user.id)
            .all()
        )
        dates = [date[0] for date in dates_list]
        releases_dates = []
        for item in dates:
            if item != None and item != "":
                releases_dates.append(item)

        today = date.today()

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
        for dated in releases_dates:
            if dated.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
                counter += 1

        for releasing in weekly_releasing:
            if releasing == today.strftime("%A"):
                counter += 1

        user.alert = counter
        db.session.commit()


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
