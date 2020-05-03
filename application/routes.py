from application import app, db, api
from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from application.models import User, Course
from flask_restplus import Resource



courseData = [
        {"courseID":"1111", "title":"PHP", "description":"Intro to PHP", "credits":"3", "term":"Term 5"},
        {"courseID":"2222", "title":"Laravel", "description":"Intro to Laravel", "credits":"3", "term":"Term 6"},
        {"courseID":"3333", "title":"Flask", "description":"Intro to Flask", "credits":"4", "term":"Term 7"},
        {"courseID":"4444", "title":"Node.js", "description":"Intro to Node.js", "credits":"4", "term":"Term 8"}
    ]

# Section 6
######################### A P I ############################

@api.route('/api', '/api/')
class GetAndPost(Resource):
    
    def get(self):
        return jsonify(User.objects.all())

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    
    def get(self,idx):
        return jsonify(User.objects(user_id=idx))


    



####################### END A P I ##########################


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "2019-2020"
    classes = Course.objects.order_by("+courseID")
    return render_template("courses.html", courseData=classes, courses=True, term=term)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1

        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!","success")
        return redirect(url_for('index'))

    return render_template("register.html", register=True, form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(f"{user.first_name} {user.last_name}, You are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

# Logout
@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course {courseTitle}", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")

    classes = None

    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)

# Test API
@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    return Response(json.dumps(jdata), mimetype="application/json")



# Function Save User manually into datbase
# @app.route("/user")
# def user():
    # User(user_id = 1, first_name = "So", last_name="Phal", email="isco23@uta.com", password="123456789").save()
    # User(user_id = 2, first_name = "Serey", last_name="Nuth", email="sereynuth@uta.com", password="123456789").save()
    # User(user_id = 3, first_name = "Sithy", last_name="Sak", email="sithysak@uta.com", password="123456789").save()
    # User(user_id = 4, first_name = "Sokun", last_name="Keo", email="sereynuth@uta.com", password="123456789").save()
    # User(user_id = 6, first_name = "Bumi", last_name="Young", email="bumiyoung@uta.com", password="123456789").save()
    # users = User.objects.all()
    # return render_template("user.html", users=users)


# Function to save course manually into database.
# @app.route("/coursedb")
# def coursedb():
#     Course(courseID="1111", title="PHP", description="Introduction to PHP", credits=3, term="Term5").save()
#     Course(courseID="2222", title="Laravel", description="Introduction to Laravel", credits=3, term="Term6").save()
#     Course(courseID="3333", title="Flask", description="Introduction to Flask", credits=4, term="Term7").save()
#     Course(courseID="4444", title="Node.js", description="Introduction to Node.js", credits=4, term="Term8").save()
#     return "Courses saved successfully !!!"

# Display all users.
@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)