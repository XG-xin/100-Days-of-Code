from flask import Flask, render_template, request
import requests
import smtplib

blog_url = "https://api.npoint.io/d1d9ec7034103579f8b3"
all_blogs = requests.get(blog_url).json()
OWN_EMAIL = <email>
OWN_PASSWORD = <password>

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", all_blogs=all_blogs)

@app.route('/about')
def about_page():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        data = request.form
        name = data['username']
        email = data['email']
        phone = data['phone']
        message = data['message']
        print(name)
        print(email)
        print(phone)
        print(message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

@app.route('/post/<int:blog_id>')
def post_page(blog_id):
    for post in all_blogs:
        if post['id'] == blog_id:
            request_post = post
    return render_template("post.html", post=request_post)

# @app.route('/form-entry', methods=['POST'])
# def receive_data():
#     name = request.form['username']
#     email = request.form['email']
#     phone = request.form['phone']
#     message = request.form['message']
#     print(name)
#     print(email)
#     print(phone)
#     print(message)
#     return "<h1>Successfully sent your message.</h1>"

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
