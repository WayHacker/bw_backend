from flask import Flask, request, url_for
from datetime import datetime
from db import Base

app = Flask(__name__)

from object import object_api
app.register_blueprint(object_api, url_prefix="/objects")

from user import user_api
app.register_blueprint(user_api, url_prefix="/users")

from assignment import assignment_api
app.register_blueprint(assignment_api, url_prefix="/assignments")

from tasks import task_api
app.register_blueprint(task_api, url_prefix="/tasks")

from assignment_task import assignment_task_api
app.register_blueprint(assignment_task_api, url_prefix="/assignments_tasks")

from instruction import instruction_api
app.register_blueprint(instruction_api, url_prefix="/instructions")

from task_instructions import instruct_task_api
app.register_blueprint(instruct_task_api, url_prefix="/task_instructions")

def say_hello_to(user: str) -> str:
    return f"""
    <div style="border: 100px solid red">
        <p>Hello, {user}!</p>
        <a href="/about">
            About Us
        </a>
    </div>
    """


def test_greets_user():
    assert "kolya" in say_hello_to("kolya")


@app.route("/")
def hello():
    if "username" not in request.args:
        return "who are you?"

    return say_hello_to(request.args["username"])


@app.route("/about")
def about_us():
    return """<div style="border: 100px solid blue">
                <p>THIS IS MULTIPAGEAPPLICATION <span id="version"></span> BY <span id="who"></span>!</p>
                <a href="/">
                    back
                </a>
                <p id="current_time"></p>
                <script>
                    const req = fetch("/about_us_data");
                    const data = req.then(response => response.json());
                    data.then(data => {
                        document.getElementById("version").innerHTML = data["version"];
                        document.getElementById("who").innerHTML = data["made_by"];
                        document.getElementById("current_time").innerHTML = `The current time is: ${data["current_time"]}`;
                    });
                </script>
            </div>
    """


@app.route("/about_us_data")
def about_us_data():
    # Do some database magic, it returns some info like a profile.

    return {
        "made_by": "Alex&Kolya",
        "current_time": datetime.now().isoformat(),
        "version": "1.0.0",
    }
