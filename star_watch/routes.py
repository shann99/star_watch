from flask import render_template, request, session, url_for, flash, redirect, get_flashed_messages, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import random, json
from star_watch.models import User, Card, Tags
from star_watch import app, db


@app.route("/",  methods=['GET','POST'])
@login_required
def index():
    user = current_user;
    if request.method == "POST":
        print("testing index call")
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')
        fav = False
        
        card = Card(title=title, image=image, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, fav=fav, user=current_user)
        
        db.session.add(card)
        db.session.commit()
        
        flash('Your new media has sucessfully been added!', category="success")
        return redirect(url_for("index"))

     #querying images where watch status equals watching
    item_list = Card.query.with_entities(Card.image).filter(Card.status=='Watching').join(User).filter(User.id==user.id).all()
    #retrieving the image itself without the extra parenthesis and commas from the query list
    images = [image[0] for image in item_list]
    #remove image if it equals default background image so it's not put into the carousel
    for image in images:
        if image == '/background.jpg':
            images.remove(image)

    random.shuffle(images)

    page = request.args.get('page', 1, type=int)
    watching_list = Card.query.filter(Card.status=='Watching').join(User).filter(User.id==user.id).order_by(Card.date_added.desc()).paginate(page=page, per_page=9)
    return render_template("index.html", user=current_user, cards=watching_list, images=images)

@app.route("/planning", methods=['GET','POST'])
@login_required
def planning():
    user = current_user
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')
        fav = False

        card = Card(title=title, image=image, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, fav=fav, user=current_user)
        db.session.add(card)
        db.session.commit()
  
        flash('Your new media has sucessfully been added!', category="success")
        return redirect(url_for("planning"))
    
    page = request.args.get('page', 1, type=int)
    planning_list = Card.query.filter(Card.status=='Planning').join(User).filter(User.id==user.id).order_by(Card.date_added.desc()).paginate(page=page, per_page=9)
    return render_template("planning.html", user=current_user, cards=planning_list)

@app.route("/paused", methods=['GET','POST'])
@login_required
def paused():
    user = current_user
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')
        fav = False;

        card = Card(title=title, image=image, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, fav=fav, user=current_user)
        db.session.add(card)
        db.session.commit()
  
        flash('Your new media has sucessfully been added!', category="success")
        return redirect(url_for("paused"))


    page = request.args.get('page', 1, type=int)
    paused_list = Card.query.filter(Card.status=='Paused').join(User).filter(User.id==user.id).order_by(Card.date_added.desc()).paginate(page=page, per_page=9)
    return render_template("paused.html", user=current_user, cards=paused_list)


@app.route("/completed", methods=['GET','POST'])
@login_required
def completed():
    user = current_user
    if request.method == "POST":
        if request.form.get('add_image_form') != "":
            image = request.form.get('add_image_form')
        else:
            image = (url_for("static", filename="background.jpg"))
        title = request.form.get('add_title')
        if request.form.get('current_ep') != "":
            current_ep = request.form.get('current_ep')
        else: 
            current_ep = 0;
        if request.form.get('total_eps') != "":
            total_eps = request.form.get('total_eps')
        else: 
            total_eps = '?'
        description = request.form.get('description')
        rating = request.form.get('rating')
        status = request.form.get('status')
        fav= False

        card = Card(title=title, image=image, current_ep=current_ep, total_eps=total_eps, status=status, description=description, rating=rating, fav=fav, user=current_user)
        
        db.session.add(card)
        db.session.commit()
        
        flash('Your new media has sucessfully been added!', category="success")
        return redirect(url_for("completed"))

    else:
        page = request.args.get('page', 1, type=int)
        completed_list = Card.query.filter(Card.status=='Completed').join(User).filter(User.id==user.id).order_by(Card.date_added.desc()).paginate(page=page, per_page=9)
        return render_template("completed.html", user=current_user, cards=completed_list)

@app.route("/account", methods=['GET','POST'])
@login_required
def account_profile():
    if request.method == "POST":
        user = current_user;
        update_user = User.query.get(user.id)

        password = request.form.get("update_password")
        pass_confirm = request.form.get("update_password_confirm")
        
        if password != pass_confirm:
                flash('Passwords must match, please try again', category='error') 
        else:
            if request.form.get('update_profile_pic') != "":
                update_user.profile_pic = request.form.get('update_profile_pic')
            if request.form.get('update_email') != "":
                update_user.email = request.form.get('update_email')
            if request.form.get('update_name') != "":
                update_user.name = request.form.get('update_name')
            if request.form.get('update_password') != "":
                password = generate_password_hash(password, method='sha256')
                update_user.password = password
            db.session.commit()
            success_message = "Your account has successfully been updated!"
            flash(success_message, category="success")
            return redirect(url_for("index"))
    return render_template("account.html", user=current_user)

@app.route("/delete_tag/<int:tag_id>/<int:card_id>", methods=['POST'])
@login_required
def delete_tag(tag_id, card_id):
    card_id = card_id
    tag = Tags.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Your tag has been deleted', category="info")
    return redirect(request.referrer)

@app.route("/update_tag/<int:tag_id>/<int:card_id>", methods=['POST'])
@login_required
def update_tag(tag_id, card_id):
    card_id = card_id
    tag = Tags.query.get(tag_id)
    if request.form.get('tag_update') != "":
        tag.name = request.form.get('tag_update')
        db.session.commit()
        flash('Your tag has been updated', category="info")
        return redirect(request.referrer)

@app.route("/edit/card/<int:card_id>", methods=['GET','POST'], strict_slashes=False)
@login_required
def editMedia(card_id):
    card = Card.query.get(card_id)
    if request.method == "POST":
        if request.form.get('edit_image_form') != "":
            card.image = request.form.get('edit_image_form')
        if request.form.get('edit_title') != "":
            card.title = request.form.get('edit_title')
        if request.form.get('edit_current_ep') != "":
            card.current_ep = request.form.get('edit_current_ep')
        if request.form.get('edit_total_eps') != "":
            card.total_eps = request.form.get('edit_total_eps')
        if request.form.get('edit_description') != "":
            card.description = request.form.get('edit_description')
        if request.form.get('edit_rating') != "":
            card.rating = request.form.get('edit_rating')
        if request.form.get('edit_status') != "":
            card.status = request.form.get('edit_status')

        card.id = card_id 
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("edit.html",  user=current_user, card_id = card_id)

@app.route('/delete/<int:card_id>', methods=['POST'])
@login_required
def delete(card_id):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()
    flash('Your media has been deleted', category="info")
    return redirect(url_for("index"))

#updating count with click of a button
@app.route('/update/<int:card_id>/<int:card_current_ep>', methods=['POST'])
@login_required
def update(card_id, card_current_ep):
    card = Card.query.get(card_id)
    card.current_ep += 1;
    db.session.commit() 
    return redirect(request.referrer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            email = request.form.get('login_address')
            password = request.form.get('login_pass')

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

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        else:
            email = request.form.get('email_address')
            name = request.form.get('name')
            password = request.form.get('pass_org')
            pass_confirm = request.form.get('pass_confirm')

            if password != pass_confirm:
                flash('Passwords must match, please try again', category='error') 
            else:
                user = User.query.filter_by(email=email).first()
                if user:
                    flash("Email already exists", category="error")

                else:
                    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
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
    
@app.route('/fav/',  methods=['POST'])
@login_required
def fav():
    if request.method == "POST":
        card = Card.query.get(request.form["card_id"])
        if request.form['card_fav'] =='true':
            card.fav = True
        db.session.commit()
        return '', 204
    
@app.route('/unfav', methods=['POST'])
@login_required
def unfav():    
    if request.method == "POST":
        card = Card.query.get(request.form["card_id"])
        if request.form['card_fav'] =='false':
            card.fav = False
        db.session.commit()
        return '', 204

@app.route('/delete_account/', methods=['POST'])
@login_required
def delete_account():
    if request.method == "POST":
        user = current_user;
        delete_user = User.query.get(user.id)

        db.session.delete(delete_user)
        db.session.commit()
        
        flash('Your account has been deleted', category="success")
        return redirect(url_for("login"))








@app.route("/tag", methods=['POST'])
@login_required
def tags():
    if request.method == 'POST':
        card = Card.query.get(request.form["card_id"])
        # print(card.id)
        test_tag = request.form.get('new_tag')
        if test_tag != "":
            if not (test_tag is None):
                print(test_tag)
                new_tag = Tags(name=test_tag, card_id=card.id)
                db.session.add(new_tag)
                db.session.commit()
                return '', 204
            else:
                print('bad1')
                flash('Something went wrong with adding a  tag, please try again', category="error")
                return '', 404
        else:
            print('bad2')
            flash ('Something went wrong with adding a  tag, please try again', category="error")
            return '', 404
    








@app.route("/planning_tag/<int:card_id>", methods=['POST'])
@login_required
def planning_tag(card_id):
    if request.method == 'POST':
        if request.form.get('add_tag') != "":
            tag = request.form.get('add_tag')
            new_tag = Tags(name=tag, card_id=card_id)
            db.session.add(new_tag)
            db.session.commit()
            return redirect(url_for("planning"))

        else:
            return redirect(url_for("planning"))
    

@app.route("/paused_tag/<int:card_id>", methods=['POST'])
@login_required
def paused_tag(card_id):
    if request.method == 'POST':
        if request.form.get('add_tag') != "":
            tag = request.form.get('add_tag')
            new_tag = Tags(name=tag, card_id=card_id)
            db.session.add(new_tag)
            db.session.commit()
            return redirect(url_for("paused"))
        else:
            return redirect(url_for("paused"))
            

@app.route("/completed_tag/<int:card_id>", methods=['POST'])
@login_required
def completed_tag(card_id):
    if request.method == 'POST':
        if request.form.get('add_tag') != "":
            tag = request.form.get('add_tag')
            new_tag = Tags(name=tag, card_id=card_id)
            db.session.add(new_tag)
            db.session.commit()
            return redirect(url_for("completed"))

        else:
            return redirect(url_for("completed"))
    

