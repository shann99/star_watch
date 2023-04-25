from flask import Flask, g
from sqlalchemy import func
from flask_login import login_user, current_user
from flask_apscheduler import APScheduler
from datetime import datetime, date
from star_watch.models import User, Card, Tags

from star_watch import app, db

scheduler = APScheduler()
# if current_user.is_authenticated():
#         g.user = current_user.get_id()
#         print(g.user)
@scheduler.task("cron", hour=9, minute=15)
def dateChecker():
    with app.app_context():

        # user=current_user
        # print(user)
        user = User.query.first()
        scheduledRelease_list = Card.query.filter(Card.release_status=="Scheduled Release").join(User).filter(User.id==user.id).order_by(Card.title.asc())
        currentRelease_list = Card.query.filter(Card.release_status=="Currently Releasing").join(User).filter(User.id==user.id).order_by(Card.title.asc())
        dates_list = Card.query.with_entities(Card.release_information).join(User).filter(User.id==user.id).all()
        dates = [date[0] for date in dates_list]
        releases_dates = []
        for item in dates:
            if item != None and item != "" and item.startswith("Weekly") is False:
                datetime_object = datetime.strptime(item, '%Y-%m-%d')
                releases_dates.append(datetime_object.date())
        today = date.today()

        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        weekly_releasing = []
        for item in dates:
            for weekday in weekdays:
                if item != None and item != "" and weekday in item:
                    weekly_releasing.append(weekday)

        counter = 0
        for dated in releases_dates:
            if dated == today:
                counter += 1

        for releasing in weekly_releasing:
            if releasing == today.strftime("%A"):
                counter += 1
        user.alert = counter
        db.session.commit()

    
if __name__== '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
    