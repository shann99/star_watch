from flask import render_template, request, session, url_for, flash, redirect, get_flashed_messages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from star_watch.models import User
from star_watch import app, db


@app.route("/", methods=['GET','POST'])
@login_required
def index():
    
    return render_template("index.html", user=current_user)

@app.route("/planning", methods=['GET','POST'])
@login_required
def planning():
    return render_template("planning.html", user=current_user)

@app.route("/paused", methods=['GET','POST'])
@login_required
def paused():
    return render_template("paused.html", user=current_user)   

@app.route("/completed", methods=['GET','POST'])
@login_required
def completed():
    return render_template("completed.html", user=current_user)

@app.route("/account", methods=['GET','POST'])
@login_required
def account_profile():
    return render_template("account.html", user=current_user)
    
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
    