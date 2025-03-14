from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Movie
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/', methods=['GET'])
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id) if movie_id else None

    if request.method == 'POST':
        name = request.form['name']
        year = int(request.form['year'])
        awards = int(request.form['awards'])
        genre = request.form['genre']

        if movie:
            movie.name = name
            movie.year = year
            movie.awards = awards
            movie.genre = genre
            flash('Movie updated successfully.', 'success')
        else:
            movie = Movie(name=name, year=year, awards=awards, genre=genre)
            db.session.add(movie)
            flash('Movie added successfully.', 'success')

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_movie.html', movie=movie)

@app.route('/edit_movie/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.year = int(request.form['year'])
        movie.awards = int(request.form['awards'])
        movie.genre = request.form['genre']
        db.session.commit()
        flash('Movie updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('edit_movie.html', movie=movie)

@app.route('/delete_movie/<int:id>', methods=['POST'])
@login_required
def delete_movie(id):
    movie = Movie.query.get_or_404(id)

    try:
        db.session.delete(movie)
        db.session.commit()
        flash('Movie deleted successfully.', 'success')
        return redirect(url_for('index'))
    except:
        flash('There was a problem deleting that movie.', 'danger')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.', 'danger')
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

