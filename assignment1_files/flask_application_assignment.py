from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

#Create App context
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Movie model representing the movies table
class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    awards = db.Column(db.Integer, nullable=False)

# Create the database and the tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    # Get all movies from the database
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id) if movie_id else None

    if request.method == 'POST':
        ## Handle updates here:  
        name = request.form['name']
        year = int(request.form['year'])
        awards = int(request.form['awards'])

        if movie:  # get values for existing movie from HTML
            movie.name = name
            movie.year = year
            movie.awards = awards
        else:  # Add new movie
            movie = Movie(name=name, year=year, awards=awards)
            db.session.add(movie)

        # Add and Commit changes to the database
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_movie.html', movie=movie)

@app.route('/edit_movie/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.year = int(request.form['year'])
        movie.awards = int(request.form['awards'])
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_movie.html', movie=movie)

@app.route('/delete_movie/<int:id>', methods=['POST'])
def delete_movie(id):
    # Get the movie by ID
    movie = Movie.query.get_or_404(id)
    
    try:
        # Delete the movie from the database
        db.session.delete(movie)
        db.session.commit()

        return redirect(url_for('index'))
    except:
        return "There was a problem deleting that movie."

if __name__ == '__main__':
    app.run(debug=True)
