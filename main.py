from flask import Flask, render_template, request

app = Flask(__name__) # create a flask app named app


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/signup/")
def signup():
    return render_template('signup.html', title="SIGN UP", information="Use the form displayed to register")


@app.route("/process-signup/", methods=['POST'])
def process_signup():
    # Let's get the request object and extract the parameters sent into local variables.
    firstname = request.form['firstname']
    surname = request.form['surname']
    dateofbirth= request.form['dateofbirth']
    residentaladdress= request.form['residentaladdress']
    nationality = request.form['nationality']
    nationalidentificationnumber = request.form['nationalidentificationnumber']
    # let's write to the database
    try:
        user = models.User(firstname=firstname, surname=surname, dateofbirth=dateofbirth, residentaladdress=residentaladdress,
                           nationality=nationality,nationalidentificationnumber=nationalidentificationnumber )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        # Error caught, prepare error information for return
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('signup.html', title="SIGN-UP", information=information)

    # If we have gotten to this point, it means that database write has been successful. Let us compose success info

    # Let us prepare success feedback information

    information = 'User by name {} {} successfully added. The login name is the email address {}.'.format(firstname,
                                                                                                          lastname,
                                                                                                          email)

    return render_template('signup.html', title="SIGN-UP", information=information)


@app.route("/login/")
def login():
    # Save off in session where we should go after login process. Session survives across requests.
    # Where to go is passed as parameter named next along with the request to /login/ URL.
    session['next_url'] = request.args.get('next', '/')  # get the next or use default '/' URL after login
    return render_template('login.html', title="SIGN IN", information="Enter login details")


@app.route("/process-login/", methods=['POST'])
def process_login():
    # Get the request object and the parameters sent.
    firstname = request.form['firstname']
    surname = request.form['surname']
    nationalidentificationnumber = request.form('nationalidentificationnumber')

    # call our custom defined function to authenticate user
    if (authenticateUser(firstname, surname, nationalidentificationnumber)):
        session['username'] = firstname
        session[
            'userroles'] = 'admin'  # just hardcoding for the sake of illustration. This should be read from database.
        return redirect(session['next_url'])
    else:
        error = 'Invalid user or password'
        return render_template('login.html', title="SIGN IN", information=error)


if __name__ == "__main__":
    app.run(port=5005)
