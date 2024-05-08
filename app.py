from flask import Flask, request
from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid

class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[Optional[str]]
    phone: Mapped[str]

   

class Object(Base):
    __tablename__ = "object"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[Optional[str]]







db_url = "postgresql://localhost/chougodno"

engine = create_engine(db_url)
app = Flask(__name__)



def say_hello_to(user: str) -> str:
    return f'''
    <div style="border: 100px solid red">
        <p>Hello, {user}!</p>
        <a href="/about">
            About Us
        </a>
    </div>
    '''

def test_greets_user():
    assert "kolya" in say_hello_to("kolya")

@app.route("/")
def hello():
    if "username" not in request.args:
        return "who are you?"

    return say_hello_to(request.args["username"])


@app.route("/about")
def about_us():
    return '''<div style="border: 100px solid blue">
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
    '''

@app.route("/about_us_data")
def about_us_data():
    # Do some database magic, it returns some info like a profile.

    return {
        "made_by": "Alex&Kolya",
        "current_time": datetime.now().isoformat(),
        "version": "1.0.0"
    }
