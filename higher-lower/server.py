from flask import Flask
import random
num = random.randint(0, 9)
print(f"The correct number is {num}")

app = Flask(__name__)

@app.route("/")
def home_page():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif'>"


@app.route("/<int:guess>")
def check_num(guess):
    if guess == num:
        return '<h2 style="color: green">You fond me!</h2>' \
               '<img src="https://media.giphy.com/media/sr8jYZVVsCmxddga8w/giphy.gif">'
    elif guess > num:
        return '<h2 style="color: purple">Too high, try again!</h2>' \
               '<img src="https://media.giphy.com/media/nR4L10XlJcSeQ/giphy.gif">'
    elif guess < num:
        return '<h2 style="color: red">Too low, try again!</h2>' \
               '<img src="https://media.giphy.com/media/4kbyKfgUIzI4M/giphy.gif">'


if __name__ == "__main__":
    # Run app in debug mode
    app.run(debug=True)
