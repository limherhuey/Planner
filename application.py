import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import *

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return redirect("/daily_tasks")

    else:
        return render_template("home.html")


@app.route("/profile")
@login_required
def profile():
    projects = retrieveAllProjects()
    tasks = retrieveAllTasks()

    return render_template("profile.html", projects=projects, tasks=tasks)


@app.route("/daily_tasks", methods=["GET", "POST"])
@login_required
def daily():
    if request.method == "GET":
        date = datetime.today().strftime("%Y-%m-%d")
        year = datetime.today().strftime("%Y")
        month = months[int(date[5] + date[6]) - 1]
        day = date[8] + date[9]
        week_day = week_days[datetime.today().weekday()]

        tasks = retrieveDailyTasks(session["user_id"], date)

        return render_template("daily.html", tasks=tasks, year=year, month=month, day=day, week_day=week_day)

    else:
        task_id = request.form.get("task_id")

        if request.form.get("complete"):
            completeDailyTask(task_id)
            return redirect("/daily_tasks")

        elif request.form.get("uncomplete"):
            uncompleteDailyTask(task_id)
            return redirect("/daily_tasks")

        elif request.form.get("delete"):
            deleteDailyTask(task_id)
            return redirect("/daily_tasks")


@app.route("/new_task", methods=["GET", "POST"])
@login_required
def newtask():
    if request.method == "GET":
        return render_template("newtask.html")

    else:
        newDailyTask(request.form.get("task"), request.form.get("notes"), request.form.get("priority"))

        flash("Task added!")
        return redirect("/daily_tasks")


@app.route("/projects", methods=["GET", "POST"])
@login_required
def projects():
    if request.method == "GET":
        projects = retrieveActiveProjects()

        return render_template("projects.html", projects=projects)

    else:
        project_id = request.form.get("project_id")

        if request.form.get("complete"):
            completeProject(project_id, datetime.today().strftime("%Y-%m-%d"))
            return redirect("/projects")

        elif request.form.get("delete"):
            deleteProject(project_id)
            return redirect("/projects")


@app.route("/new_project", methods=["GET", "POST"])
@login_required
def newproject():
    if request.method == "GET":
        today = datetime.today().strftime("%Y-%m-%d")
        return render_template("newproject.html", today=today)

    else:
        newProject(request.form.get("title"), request.form.get("notes"), request.form.get("deadline"))

        flash("Project added!")
        return redirect("/projects")


@app.route("/all_projects", methods=["GET", "POST"])
@login_required
def allprojects():
    if request.method == "GET":
        projects = retrieveAllProjects()

        return render_template("allprojects.html", projects=projects)

    else:
        project = retrieveProject(request.form.get("project_id"))

        return render_template("editproject.html", project=project)


@app.route("/edit_project", methods=["GET", "POST"])
@login_required
def editproject():
    if request.method == "GET":
        flash("Please select a project to edit.")
        return redirect("/all_projects")

    else:
        project_id = request.form.get("project_id")

        if request.form.get("title"):
            title = request.form.get("title")
        else:
            title = request.form.get("orititle")

        if request.form.get("notes"):
            notes = request.form.get("notes")
        else:
            notes = request.form.get("orinotes")

        if request.form.get("deadline"):
            deadline = request.form.get("deadline")
        else:
            deadline = request.form.get("orideadline")

        if request.form.get("completed") == "Yes":
            completed = 1
            enddate = datetime.today().strftime("%Y-%m-%d")
        else:
            completed = 0
            enddate = None

        editStatedProject(project_id, title, notes, deadline, enddate, completed)

        flash("Changes saved!")
        return redirect("all_projects")


@app.route("/login", methods=["GET", "POST"])
def login():
    # forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    else:
        user = retrieveUser(request.form.get("username"))
        if not user or not check_password_hash(user[0][2], request.form.get("password")):
            return render_template("login.html", error = 1)

        # remember which user logged in
        session["user_id"] = user[0][0]

        flash("Logged in as " + user[0][1] + "!")
        return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    else:
        user = retrieveUser(request.form.get("username"))
        if user and user[0][1] == request.form.get("username"):
            return render_template("register.html", error=1)

        elif request.form.get("password") != request.form.get("cpassword"):
            return render_template("register.html", error=2)

        insertUser(request.form.get("username"), request.form.get("password"))

        # then automatically log user in
        user = retrieveUser(request.form.get("username"))
        session["user_id"] = user[0][0]

        flash("Registered successfully, logged in as " + user[0][1] + "!")
        return redirect("/")


@app.route("/clock")
def clock():
    return render_template("clock.html")


@app.route("/stopwatch")
def stopwatch():
    return render_template("stopwatch.html")


@app.route("/timer")
def timer():
    return render_template("timer.html")