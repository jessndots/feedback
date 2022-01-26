from crypt import methods
from flask import Flask, request, render_template, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 
debug = DebugToolbarExtension(app)

from forms import RegisterForm, LoginForm, FeedbackForm

from models import db, connect_db, User, Feedback
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True       
      
connect_db(app)


@app.route("/")
def redirect_register():
    """Redirect to register"""
    return redirect("/register")

@app.route("/register", methods = ["GET", "POST"])
def register_user():
    """Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name."""
    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = User.register(first_name, last_name, email, username, password)
        db.session.add(user)
        db.session.commit()

        flash("You have successfully created an account.")
        session["username"] = user.username
        return redirect(f"/users/{username}")
    else: 
        return render_template("register_user.html", form=form)


@app.route("/users/<username>")
def show_user(username):
    if "username" in session: 
        if session["username"] == username:
            user = User.query.get_or_404(session['username'])
            return render_template("user.html", user=user)
        else: 
            flash("You do not have permission to view other user accounts.")
            un = session["username"]
            return redirect(f"/users/{un}")
    else:
        flash("You must be logged in to view.")
        return redirect("/login")


@app.route("/login", methods=['GET', 'POST'])
def login_user():
	"""Produce login form or handle login."""
	form = LoginForm()
	if form.validate_on_submit():
		name = form.username.data
		pwd = form.password.data
		# authenticate will return a user or False
		user = User.authenticate(name, pwd)
		if user:
			session["username"] = user.username
			# keep logged in
			return redirect(f"/users/{user.username}")
		else:
			form.username.errors = ["Invalid username or password"]
	return render_template("login_user.html", form=form)


@app.route("/logout")
def logout_user():
    """Logs user out and redirects to homepage."""
    session.pop("username")
    return redirect("/")

@app.route("/users/<username>/delete")
def delete_user(username):
    """Deletes user and user's feedback from db, clears username from session, and redirects to /"""
    if "username" in session:
        feedback = User.query.get_or_404(username)
        if session['username'] == username:     
            User.query.filter_by(username=username).delete()
            db.session.commit()
            flash("User successfully deleted.")
            session.pop("username")
            return redirect("/")
        else: 
            flash("You do not have permission to delete other user accounts.")
            return redirect(f"/users/{session['username']}")
    else: 
        flash('You must be logged in to delete a user.')
        return redirect("/login")



@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Produce add feedback form or handle feedback"""
    if "username" in session:
        if session['username'] == username:     
            form = FeedbackForm()
            if form.validate_on_submit():
                title = form.title.data
                content = form.content.data

                feedback = Feedback(title=title, content=content, username=username)
                db.session.add(feedback)
                db.session.commit()

                flash("Feedback submitted.")
                return redirect(f"/users/{username}")
            else: 
                return render_template("add_feedback.html", form=form)
        else: 
            flash("You can not submit feedback for other users.")
            return redirect(f"/users/{session['username']}")
    else: 
        flash('You must be logged in to submit feedback.')
        return redirect("/login")

@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """Produce edit feedback form or handle feedback edits"""
    if "username" in session:
        feedback = Feedback.query.get_or_404(feedback_id)
        if session['username'] == feedback.username:     
            form = FeedbackForm()
            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data

                db.session.add(feedback)
                db.session.commit()

                flash("Feedback successfully edited.")
                return redirect(f"/users/{feedback.username}")
            else: 
                form.title.data = feedback.title
                form.content.data = feedback.content
                return render_template("edit_feedback.html", form=form)
        else: 
            flash("You can not edit feedback for other users.")
            return redirect(f"/users/{session['username']}")
    else: 
        flash('You must be logged in to edit feedback.')
        return redirect("/login")
        
@app.route("/feedback/<feedback_id>/delete")
def delete_feedback(feedback_id):
    """deletes feedback from db and redirects to user page"""
    if "username" in session:
        feedback = Feedback.query.get_or_404(feedback_id)
        if session['username'] == feedback.username:     
            Feedback.query.filter_by(id=feedback_id).delete()
            db.session.commit()
            flash("Feedback successfully deleted.")
            return redirect(f"/users/{session['username']}")
        else: 
            flash("You can not delete feedback for other users.")
            return redirect(f"/users/{session['username']}")
    else: 
        flash('You must be logged in to delete feedback.')
        return redirect("/login")

