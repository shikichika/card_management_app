from crypt import methods
from datetime import timedelta
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
import yaml
from helper import hash


# FLASK_APP=view.py flask run --debugger --reload
app = Flask(__name__)

# for session
app.secret_key = 'abcdefghijklmn'
app.permanent_session_lifetime = timedelta(minutes=30)

# configure db
db = yaml.safe_load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/index', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        #search cards
        original_search_name = request.form.get("search_name")
        search_name = "%" + original_search_name + "%"
        my_cursor = mysql.connection.cursor()
        my_cursor.execute(
            "SELECT cards.id, cards.name, cards.due_date_on, genres.genre FROM cards JOIN genres ON cards.genre_id = genres.id WHERE cards.user_id = %s AND cards.name LIKE %s", (session["user_id"], search_name))
        cards = my_cursor.fetchall()
        my_cursor.close()

    else:
        # Get cards data
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT cards.id, cards.name, cards.due_date_on, genres.genre FROM cards JOIN genres ON cards.genre_id = genres.id WHERE cards.user_id = %s", [
            session["user_id"]])

        cards = my_cursor.fetchall()
        my_cursor.close()

    return render_template("index.html", cards=cards)


@app.route('/card_update/<id>', methods=["GET", "POST"])
def card_update(id):
    if request.method == "POST":

        # If input is update
        if request.form['action'] == 'update':
            # Get from values from user
            card_name = request.form.get('card_name')
            card_genre = request.form.get('card_genre')
            due_date = request.form.get('due_date')

            if not card_name:
                    
                return redirect(url_for("card_update", id = id)) 
        

            try: 

                # Get genre_id
                my_cursor = mysql.connection.cursor()
                my_cursor.execute(
                    "SELECT id FROM genres WHERE genre = %s AND user_id = %s", (card_genre, session["user_id"]))
                genre_id = my_cursor.fetchone()[0]

                # If due_date is null
                if not due_date:
                    my_cursor.execute("UPDATE cards set name = %s, due_date_on = NULL, genre_id = %s WHERE id = %s AND user_id = %s", (
                        card_name, genre_id, id, session["user_id"]))
                # If due_date exits
                else:
                    my_cursor.execute("UPDATE cards set name = %s, due_date_on = %s, genre_id = %s WHERE id = %s AND user_id = %s", (
                        card_name, due_date, genre_id, id, session["user_id"]))

                #commit and close
                mysql.connection.commit()
                my_cursor.close()
            except:
                flash("Please select genre")
                redirect(url_for("card_update", id = id))

            return redirect("/index")

        # If action is delete
        elif request.form['action'] == 'delete':

            # Delete recode
            my_cursor = mysql.connection.cursor()
            my_cursor.execute(
                "DELETE FROM cards WHERE id = %s AND user_id = %s", (id, session["user_id"]))
            mysql.connection.commit()
            my_cursor.close()
            return redirect(url_for("index"))

        # Return to index page
        elif request.form['action'] == 'cancell':
            return redirect(url_for("index"))

    else:
        # Get the card detail
        my_cursor = mysql.connection.cursor()
        my_cursor.execute(
            "SELECT cards.id, cards.name, cards.due_date_on, genres.genre  FROM cards JOIN genres on cards.genre_id = genres.id WHERE cards.user_id = %s AND cards.id = %s", (session['user_id'], id))
        card_detail = my_cursor.fetchall()
        my_cursor.close()
        # Reset cursor and get options of genres for select
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT id, genre FROM genres WHERE user_id = %s", [
                          session['user_id']])
        genres = my_cursor.fetchall()
        my_cursor.close()

        return render_template("/card_update.html", card_detail=card_detail[0], genres=genres)


@app.route('/create_recode', methods=["GET", "POST"])
def create_recode():
    if request.method == "POST":

        # If input is update
        if request.form['action'] == 'create':
            # Get from values from user
            card_name = request.form.get('card_name')
            card_genre = request.form.get('card_genre')
            due_date = request.form.get('due_date')

            if not card_name:
                flash("Card name must be")
                return redirect(url_for("create_recode"))
            
            try:
                # Get genre_id
                my_cursor = mysql.connection.cursor()
                my_cursor.execute(
                    "SELECT id FROM genres WHERE genre = %s AND user_id = %s", (card_genre, session["user_id"]))
                genre_id = my_cursor.fetchone()[0]
            except:
                flash("Please select genre")
                return redirect(url_for("create_recode"))

            # If due_date is null
            if not due_date:
                my_cursor.execute("INSERT INTO cards  (name, due_date_on, genre_id, user_id) VALUES (%s, NULL, %s, %s)", (
                    card_name, genre_id, session["user_id"]))
            # If due_date exits
            else:
                my_cursor.execute("INSERT INTO cards (name, due_date_on, genre_id, user_id) VALUES (%s, %s, %s, %s)", (
                    card_name, due_date, genre_id, session["user_id"]))

            #commit and close
            mysql.connection.commit()
            my_cursor.execute("SELECT cards.id, cards.name, cards.due_date_on, genres.genre FROM cards JOIN genres ON cards.genre_id = genres.id WHERE cards.user_id = %s", [
            session["user_id"]])

            cards = my_cursor.fetchall()
            my_cursor.close()

            
            return redirect(url_for("index"))

        # Return to index page
        elif request.form['action'] == 'cancell':
            return redirect(url_for("index"))

    else:

        # Reset cursor and get options of genres for select
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT id, genre FROM genres WHERE user_id = %s", [
                          session['user_id']])
        genres = my_cursor.fetchall()
        my_cursor.close()

        return render_template("/card_create.html", genres=genres)


@app.route('/create_genre', methods=["GET", "POST"])
def create_genre():
    if request.method == "POST":

        if request.form['action'] == "create":
            
            genre = request.form.get('genre')

            if not genre:
                flash("Must genre name")
                return redirect(url_for("create_genre"))
            else:
                my_cursor = mysql.connection.cursor()
                my_cursor.execute(
                    "INSERT INTO genres(genre, user_id) VALUES(%s, %s)", (genre, session["user_id"]))
                mysql.connection.commit()
                my_cursor.close()
                return redirect(url_for("index"))

        elif request.form['action'] == "cancell":
            return redirect(url_for("index"))

    else:
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT id, genre FROM genres WHERE user_id = %s", [
                          session['user_id']])
        genres = my_cursor.fetchall()
        my_cursor.close()

        return render_template("genre_create.html", genres=genres)


@app.route('/delete_genre/<id>')
def delete_genre(id):
    try:
        my_cursor = mysql.connection.cursor()
        my_cursor.execute(
            "DELETE FROM genres WHERE id = %s AND user_id = %s", (id, session["user_id"]))
        mysql.connection.commit()
        my_cursor.close()
        return redirect(url_for("create_genre"))
    except:
        flash("You can't delete this genre while it is used", 'danger')
        return redirect(url_for("create_genre"))


@app.route('/register', methods=["GET", "POST"])
def register():
    print(request.method)
    if request.method == "POST":

        # forget session
        session.clear()

        # Get data from form
        name = request.form.get('name')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

        # Ensure name, password and re_password are not null
        if not name or not password or not re_password:
            
            flash("Name and password required")
            return redirect(url_for("register"))
        # Ensure password and re_password are the same
        elif password != re_password:
            
            flash("Passwords are not match")
            return redirect(url_for("register"))
        # Ensure password is over 6
        elif len(password) < 6 or len(password) > 12:
           
            flash("Password has to be more than 5 and less than 12")
            return redirect(url_for("register"))
        
        #Set hashed password
        hash_password = hash(name, password)
         # set cursor
        my_cursor = mysql.connection.cursor()
        # For ensuring if the same username and password doesn't exit
        result_value = my_cursor.execute(
            "SELECT id FROM users WHERE name = %s AND password = %s", (name, hash_password))
        
        # Ensure if the same username and password doesn't exit
        if result_value >= 1:
            my_cursor.close()
            flash("You can't use the username")
            return redirect(url_for("register"))

        add_user = ("INSERT INTO users(name, password) VALUES(%s, %s)")
        
        user = (name, hash_password)
        my_cursor.execute(add_user, user)
        mysql.connection.commit()

        my_cursor.execute(
            "SELECT id FROM users WHERE name = %s AND password = %s", (name, hash_password))
        session['user_id'] = my_cursor.fetchone()[0]
        my_cursor.close()

        return redirect("/index")
    else:
        
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Reset any session
        session.clear()
        # Get information from user
        name = request.form.get('name')
        password = request.form.get('password')

        #Get hashed password
        hash_password = hash(name, password)

        # set cursor
        my_cursor = mysql.connection.cursor()
        # Query user
        result_value = my_cursor.execute(
            "SELECT * FROM users WHERE name = %s AND password = %s", (name, hash_password))
        if not name or not password:
            my_cursor.close()
            flash("Name is required")
            return redirect(url_for("login"))
        elif not result_value:
            my_cursor.close()
            flash("Not mutch username or password")
            return redirect(url_for("login"))

        session['user_id'] = my_cursor.fetchone()[0]
        print(session['user_id'])
        my_cursor.close()
        return redirect("/index")
    else:
        session.clear()
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
