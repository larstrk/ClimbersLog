import os
import matplotlib.pyplot as plt
import base64


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, is_strong_password, get_username, calculate_weighted_kpi, convert_to_int

from io import BytesIO
from datetime import datetime

# Initialize Matplotlib in the main thread
plt.switch_backend('agg')

# from helpers import apology, login_required, is_strong_password

# Configure application
app = Flask(__name__)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["STATIC_FOLDER"] = "static"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///climberslog.db")

# Initialize Matplotlib in the main thread

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """Get Information about Gym."""
    # Query the database for unique cities from the gyms table
    cities = db.execute("SELECT DISTINCT city FROM gyms ORDER BY city ASC")

    # Get the user's name from the database based on their session
    user_username = get_username(session)

    # Pass the list of cities to the template
    return render_template('index.html', cities=cities, user_username=user_username)


@app.route("/gyms", methods=["POST"])
def search_gyms():
    selected_city = request.form.get('city')

    # Use selected_city to query the database for gyms in that city
    # You'll need to implement this query based on your database structure

    # Example query:
    gyms = db.execute("SELECT * FROM gyms WHERE city=? ORDER BY name ASC", (selected_city,))

    # Get the user's name from the database based on their session
    user_username = get_username(session)

    # Return the list of gyms to your template for rendering
    return render_template('gyms.html', selected_city=selected_city, gyms=gyms, user_username=user_username)




@app.route("/sessions", methods=["GET", "POST"])
@login_required
def sessions():
    # Get the user's name from the database based on their session
    user_username = get_username(session)

    # Retrieve session data from the database with gym names
    sessions = db.execute("""
        SELECT s.*, g.name AS gym_name
        FROM sessions AS s
        JOIN gyms AS g ON s.gym_id = g.id
        WHERE user_id = :user_id
        ORDER BY date DESC
    """, user_id=session["user_id"])


    return render_template("sessions.html", sessions=sessions, user_username=user_username)

@app.route("/deletesession/<int:session_id>", methods=["GET"])
@login_required
def deletesession(session_id):
    # Ensure that the session ID is valid (e.g., it exists in the database)

    # Delete the session from the database (you'll need to implement this)
    db.execute("DELETE FROM sessions WHERE id = :session_id", session_id=session_id)

    # Redirect to the sessions page or display a success message
    return redirect("/sessions")


@app.route("/addsession", methods=["GET", "POST"])
def addsession():

    # Get the user's name from the database based on their session
    user_username = get_username(session)

    if request.method == "POST":
        # Get data from the form
        date = request.form.get("date")
        gym_id = int(request.form.get("gym"))
        print("gym_id:", gym_id)  # Debug statement to check the value of gym_name
        # Retrieve gym_id and gym_levels from the database
        gym_data = db.execute("SELECT name, levels FROM gyms WHERE id = ?", gym_id)

        gym_name = gym_data[0]["name"]
        print(f'Gym name: {gym_name}')
        gym_levels = gym_data[0]["levels"]
        print(f'Gym levels: {gym_levels}')

        # Convert form fields to integers with default value 0 for empty fields
        level1 = convert_to_int(request.form.get("level1"))
        level2 = convert_to_int(request.form.get("level2"))
        level3 = convert_to_int(request.form.get("level3"))
        level4 = convert_to_int(request.form.get("level4"))
        level5 = convert_to_int(request.form.get("level5"))
        level6 = convert_to_int(request.form.get("level6"))
        level7 = convert_to_int(request.form.get("level7"))
        level8 = convert_to_int(request.form.get("level8"))

        # Calculate the KPI
        kpi = calculate_weighted_kpi(level1,level2,level3,level4,level5,level6,level7,level8,gym_levels)

        # Insert the session data into the database
        db.execute(
            "INSERT INTO sessions (user_id, gym_id, date, level1, level2, level3, level4, level5, level6, level7, level8, kpi) "
            "VALUES (:user_id, :gym_id, :date, :level1, :level2, :level3, :level4, :level5, :level6, :level7, :level8, :kpi)",
            user_id=session["user_id"],
            gym_id=gym_id,
            date=date,
            level1=level1,
            level2=level2,
            level3=level3,
            level4=level4,
            level5=level5,
            level6=level6,
            level7=level7,
            level8=level8,
            kpi=kpi,
        )

        # Redirect to the sessions page or display a success message
        return redirect("/sessions")

    # Fetch gyms from the database
    gyms = db.execute("SELECT id, name FROM gyms ORDER BY city, name")
    # You should add code to fetch gyms and levels here

    return render_template("addsession.html", gyms=gyms, levels=range(1, 9), user_username=user_username)




@app.route("/history", methods=["GET"])
@login_required
def history():
    
    # Get the user's name from the database based on their session
    user_username = get_username(session)

    # Retrieve KPI data from the database (modify this query as needed)
    kpi_data = db.execute("SELECT date, kpi FROM sessions WHERE user_id = :user_id", user_id=session["user_id"])

    # Extract dates and KPI values from the query result, and convert dates to datetime objects
    dates = [datetime.strptime(entry["date"], "%Y-%m-%d") for entry in kpi_data]
    kpi_values = [entry["kpi"] for entry in kpi_data]

    # Create a plot
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.plot(dates, kpi_values, marker='o', linestyle='-')
    plt.xlabel("Date")
    plt.ylabel("KPI")
    # Customize the grid
    plt.grid(True, axis='y')  # Show horizontal grid lines only for the y-axis
    plt.grid(False, axis='x')  # Hide vertical grid lines for the x-axis

    # Save the plot as an image in memory
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Encode the image to base64 for embedding in the HTML
    img_data = base64.b64encode(img_buf.read()).decode()

    return render_template("history.html", user_username=user_username, img_data=img_data)
    


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username does not already exist
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("Username already exists", 400)

        # Ensure password was submitted and confirmPassword matches Passoword
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        if not is_strong_password(request.form.get("password")):
            return apology("Password does not meet the strength requirements", 400)

        # Hash the password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Insert the new user into the database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hashed_password)

        # Check if the registration was successful
        if not result:
            return apology("Registration failed", 403)

        # Log in the user after successful registration
        session["user_id"] = result

        # Redirect to the home page or a success page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/sessions")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")