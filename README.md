
# Planner
> This project uses Flask (Python), SQL, HTML, CSS, and JavaScript.

Planner is a web-based application which allows users to customise their own daily to-do list as well as long term projects,
it also has other utilities that users can take advantage of to get their work done.

### Details of components:
* Homepage
    - the main page of the website, with a brief description of the website and its different pages

* Register/Login
    - users may create a new account and log in

* Daily Tasks
    - only the tasks for the current date will be shown here, along with today's date
    - users can mark a task as completed, which will push the task to the very bottom and highlight it in a darker colour so users can easily focus on tasks that have not been completed yet
    - users can add or delete new tasks for the day and write short descriptions/notes for them if needed
    - tasks have priority ratings, which will determine the order in which they are shown so users know which tasks to complete first (higher priority tasks arranged nearer to the top)

* Projects
    - for long-term tasks that outlive the span of a day's work
    - active (uncompleted) projects will be shown on this page, with their respective start dates and deadlines
    - users can mark a project as completed, delete, or add a project at any point in time
    - users can see all their projects (active or otherwise) on a separate page, where they may also edit any project; like the daily tasks, completed projects will be in a darker highlight and shown below uncompleted ones

* Profile
    - a history page for the user, displaying all of the user's projects and tasks
    - users may use this page to assess their everyday productivity or use it as an overview

* Clock
    - this page displays today's date and current time taking up a large part of the screen, designed to be simple so as to be a suitable page for users to park on when working on a task or project

* Timer
    - a minimalistic design of a timer, equipped with all the basic functions of a timer
    - users can enter any length of time they wish into the timer
    - time is automatically calibrated to convention if minutes and seconds entered are more than 60
    - the text flashes red for up to 3 minutes when the time is up

* Stopwatch
    - a minimalistic design of a stopwatch, equipped with all the basic functions of a stopwatch

* Footer
    - displays a motivational quote for users
