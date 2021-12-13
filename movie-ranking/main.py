from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests
import os


WTF_CSRF_SECRET_KEY = 'randomstring'
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
API_KEY = os.environ.get('MOVIE_DB_API_KEY')
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/original"

#CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies_list.db"
db=SQLAlchemy(app)

#CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=True)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.Text(500), unique=False, nullable=True)
    img_url = db.Column(db.String(250), unique=False, nullable=True)


db.create_all()


#CREATE EDIT FORM
class EditForm(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g. 7.5", validators=[NumberRange(min=0, max=10, message='Invalid Rating')])
    review = StringField(label='Your Review')
    submit = SubmitField(label='Done')



#CREATE ADD FORM
class AddForm(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')

@app.route("/")
def home():
    # all_movies = db.session.query(Movie).all()
    # This line creates a list of all the movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    edit_form = EditForm()
    id = request.args.get('id')
    updated_movie = Movie.query.get(id)

    if request.method == 'POST':

        updated_movie.rating = edit_form.rating.data
        updated_movie.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=updated_movie, form=edit_form)


@app.route("/delete")
def delete():
    id = request.args.get('id')
    deleted_movie = Movie.query.get(id)
    db.session.delete(deleted_movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        # SEARCH THEMOVIEDB
        parameters = {
            "api_key": API_KEY,
            "query": movie_title
        }
        response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=parameters)
        movie_data = response.json()["results"]
        print(movie_data)
        return render_template("select.html", movies=movie_data)
    return render_template('add.html', form=add_form)


@app.route('/search', methods=['POST', 'GET'])
def search():
    id = request.args.get('id')
    if id:
        parameters = {
            "api_key": API_KEY,
        }
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{id}", params=parameters)
        movie = response.json()
        new_movie = Movie(
            title=movie['title'],
            year=movie['release_date'].split("-")[0],
            description=movie['overview'],
            img_url=f"{MOVIE_DB_IMAGE_URL}{movie['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)

