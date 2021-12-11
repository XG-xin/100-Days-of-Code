from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

all_books = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # new_book = {
        # "title": request.form['title'],
        # "author": request.form['author'],
        # "rating": request.form['rating']
        # }
        # all_books.append(new_book)
        new_book = Books(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        book_id = request.form["id"]
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()

        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_select = Books.query.get(book_id)
    # print(book_select.title)
    return render_template('edit.html', book=book_select)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    print(book_to_delete.title)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
