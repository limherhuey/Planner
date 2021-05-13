
import sqlite3
from flask import Flask, flash, session, redirect
from flask_session import Session
from functools import wraps
from werkzeug.security import generate_password_hash



months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]



def login_required(f):
    # http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



# All functions for SQL queries:

def insertUser(username, password):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    h = generate_password_hash(password)
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, h))
    c.commit()
    c.close()


def retrieveUser(username):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = db.fetchall()
    c.close()
    return user


def newDailyTask(task, notes, priority):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("INSERT INTO dailytasks (user_id, priority, task, notes, completed) VALUES (?, ?, ?, ?, ?)", (session["user_id"], priority, task, notes, 0))
    c.commit()
    c.close()


def retrieveDailyTasks(user_id, date):
    c = sqlite3.connect("planner.db")
    # row_factory returns SQL query as a dictionary per row
    c.row_factory = sqlite3.Row
    db = c.cursor()
    db.execute("SELECT id, priority, task, notes, completed FROM dailytasks WHERE user_id = ? AND date = ? ORDER BY completed, priority", (user_id, date))
    tasks = db.fetchall()
    c.close()
    return tasks


def retrieveAllTasks():
    c = sqlite3.connect("planner.db")
    c.row_factory = sqlite3.Row
    db = c.cursor()
    db.execute("SELECT id, priority, task, notes, completed, date FROM dailytasks WHERE user_id = ? ORDER BY date, completed, priority", (session["user_id"],))
    tasks = db.fetchall()
    c.close()
    return tasks


def completeDailyTask(task_id):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("UPDATE dailytasks SET completed = 1 WHERE id = ?", (task_id,))
    c.commit()
    c.close()


def uncompleteDailyTask(task_id):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("UPDATE dailytasks SET completed = 0 WHERE id = ?", (task_id,))
    c.commit()
    c.close()


def deleteDailyTask(task_id):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("DELETE FROM dailytasks WHERE id = ?", (task_id,))
    c.commit()
    c.close()


def newProject(title, notes, deadline):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("INSERT INTO projects (user_id, title, notes, deadline, completed) VALUES (?, ?, ?, ?, ?)", (session["user_id"], title, notes, deadline, 0))
    c.commit()
    c.close()


def retrieveActiveProjects():
    c = sqlite3.connect("planner.db")
    c.row_factory = sqlite3.Row
    db = c.cursor()
    db.execute("SELECT id, title, notes, startdate, deadline FROM projects WHERE user_id = ? AND completed = 0 ORDER BY deadline", (session["user_id"],))
    projects = db.fetchall()
    c.close()
    return projects


def retrieveAllProjects():
    c = sqlite3.connect("planner.db")
    c.row_factory = sqlite3.Row
    db = c.cursor()
    db.execute("SELECT id, title, notes, startdate, deadline, enddate, completed FROM projects WHERE user_id = ? ORDER BY completed, enddate, deadline", (session["user_id"],))
    projects = db.fetchall()
    c.close()
    return projects


def retrieveProject(project_id):
    c = sqlite3.connect("planner.db")
    c.row_factory = sqlite3.Row
    db = c.cursor()
    db.execute("SELECT id, title, notes, deadline, completed FROM projects WHERE id = ?", (project_id,))
    project = db.fetchall()
    c.close()
    return project


def completeProject(project_id, enddate):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("UPDATE projects SET completed = 1, enddate = ? WHERE id = ?", (enddate, project_id))
    c.commit()
    c.close()


def deleteProject(project_id):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("DELETE FROM projects WHERE id = ?", project_id)
    c.commit()
    c.close()


def editStatedProject(project_id, title, notes, deadline, enddate, completed):
    c = sqlite3.connect("planner.db")
    db = c.cursor()
    db.execute("UPDATE projects SET title = ?, notes = ?, deadline = ?, completed = ? WHERE id = ?", (title, notes, deadline, completed, project_id))
    c.commit()
    c.close()
