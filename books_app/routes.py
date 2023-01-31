"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from books_app.models import Book, Author, Genre, User
from books_app.forms import BookForm, AuthorForm, GenreForm, UserForm

# Import app and db from events_app package so that we can run app
from books_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_books = Book.query.all()
    all_users = User.query.all()
    return render_template('home.html', 
        all_books=all_books, all_users=all_users)

@main.route('/create_book', methods=['GET', 'POST'])
def create_book():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            publish_date=form.publish_date.data,
            author=form.author.data,
            audience=form.audience.data,
            genres=form.genres.data
        )
        db.session.add(new_book)
        db.session.commit()

        flash('New book was created successfully.')
        return redirect(url_for('main.book_detail', book_id=new_book.id))
    return render_template('create_book.html', form=form)

@main.route('/create_author', methods=['GET', 'POST'])
def create_author():
    # Make an AuthorForm instance
    form_for_author = AuthorForm()
    # If the form was submitted and is valid, create a new Author object
    if form_for_author.validate_on_submit():
        new_author = Author(
            name = form_for_author.name.data,
            biography =form_for_author.biography.data,
        )
    # and save to the database, then flash a success message to the user and
        db.session.add(new_author)
        db.session.commit()
        flash("New author successfully created!")
        # redirect to the homepage
        return redirect(url_for('main.homepage'))
    # Send the form object to the template, and use it to render the form
    # fields
    return render_template('create_author.html', form=form_for_author)

@main.route('/create_genre', methods=['GET', 'POST'])
def create_genre():
    # Make a GenreForm instance
    form_for_genre = GenreForm()
    
    # If the form was submitted and is valid, create a new Genre object
    if form_for_genre.validate_on_submit():
        new_genre = Genre(
            name = form_for_genre.name.data
        )
    # and save to the database, then flash a success message to the user and
        db.session.add(new_genre)
        db.session.commit()
        flash("New genre successfully created!")
    # redirect to the homepage
        return redirect(url_for('main.homepage')) 
    # Send the form object to the template, and use it to render the form
    # fields
    return render_template('create_genre.html', form=form_for_genre)

@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # STRETCH CHALLENGE: Fill out the Create User route
    return "Not Yet Implemented"

@main.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)

    # If the form was submitted and is valid, update the fields in the 
    # Book object and save to the database, then flash a success message to the 
    # user and redirect to the book detail page
    if form.validate_on_submit():
        book.title = form.title.data,
        book.publish_date = form.publish_date,
        book.author = form.author.data,
        book.audience = form.audience.data,
        book.genres = form.genres.data,

        db.session.commit()
        flash("Book Updated!")
        return redirect(url_for('main.book_detail', book_id=-book_id))

    return render_template('book_detail.html', book=book, form=form)

@main.route('/profile/<username>')
def profile(username):
    # Make a query for the user with the given username, and send to the
    # template
    user = User.query.filter_by(username=username)
    form_for_user = UserForm()

    if form_for_user.validate_on_submit():
        user.username = form_for_user.data
        db.session.commit
        flash("Success!")
        return redirect(url_for('main.homepage'))
    return render_template('profile.html', username=username)
    # STRETCH CHALLENGE: Add ability to modify a user's username or favorite 
    # books
    
