# DDWT24_w3

This assignment is a web application that connects to an SQLite database to manage movies. The user can view the list of movies, add new movies and delete or edit movies from the database. Access to these features is protected by a user authentication system, ensuring that only registered and logged-in users can perform these actions.

Features
User Authentication: The application has a user registration and login system. Only logged-in users can access the movie database features.

Movies Database
Usercan view a list of movies stored in the database,
add new movies to the database,
edit details of an existing movie,
and delete a movie from the database.

API Support
All interactions with the movies (view, add, edit, delete) are exposed via an API using RESTful endpoints. The API is secured using JWT (JSON Web Token) authentication.

Error Handling
The application includes a custom 404 error handler that returns an error message when users attempt to access a non-existent page or endpoint.

Installation
1. Clone this repository to your local machine:
git clone <repository_url>
cd <repository_directory>

2. Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate

3. Install the required dependencies:
pip install -r requirements.txt

4. Set up the database:
flask db init
flask db migrate -m "First migration"
flask db upgrade

5. Run the application:
flask run

The application will be running at http://127.0.0.1:5000.

Testing the API
You can test the API using the test_api.py script. The script shows how to log in a user, access the list of movies, and add, update, and delete movies.

To test, run the script:
python3 test_api.py

(Ensure that the application is running before running the script)

