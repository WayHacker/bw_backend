from flask import Flask, request

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
    print(request.args)
    return '''<div style="border: 100px solid blue">
                <p>THIS IS A MULTIPAGEAPPLICATION BY ALEX & KOLYA!</p>
                <a href="/">
                    back
                </a>
            </div>
    '''
