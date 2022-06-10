from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

# Initilize the database
db = SQLAlchemy(app)

# Create db model

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    e_mail = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(10), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # Create a function to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/home')
def home():
    stuff = 'Test <strong> BOLD </strong>'
    return render_template("home.html", stuff = stuff)

@app.route('/dashboard')
def dashboard():
    names = ['test', 'test1']
    return render_template('dashboard.html', names = names)


@app.route('/users', methods =['POST', 'GET'])
def users():
    
    if request.method == 'POST':
        
        user_name_check = request.form.get('name')
        e_mail_check = request.form.get('e_mail')
        password_check = request.form.get('password')

        if not user_name_check or not e_mail_check or not password_check:
            error_statement = 'Please fill all the forms.'
            users = Users.query.order_by(Users.date_created)
            return render_template('users.html', error_statement = error_statement, user_name_check = user_name_check, 
            e_mail_check = e_mail_check, password_check = password_check, users = users)
        else:
            user_name = request.form['name']
            user_e_mail = request.form['e_mail']
            user_password = request.form['password']
            new_user = Users(name= user_name, e_mail = user_e_mail , password = user_password )
            # push to database
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect('/users')
            except:
                return "There was an error adding the user..."
            return "you clicked the button"
    else:
        users = Users.query.order_by(Users.date_created)
        return render_template('users.html', users = users)


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    user_to_update = Users.query.get_or_404(id)
    users = Users.query.order_by(Users.date_created)
    if request.method == 'POST':

        user_name_check = request.form.get('name')
        e_mail_check = request.form.get('e_mail')
        password_check = request.form.get('password')

        if not user_name_check or not e_mail_check or not password_check:
            error_statement = 'Please fill all the forms.'
            users = Users.query.order_by(Users.date_created)
            return render_template('users.html', error_statement = error_statement, user_name_check = user_name_check, 
            e_mail_check = e_mail_check, password_check = password_check, users = users)
        else:
            try:
                user_to_update.name = request.form['name']
                user_to_update.e_mail = request.form['e_mail']
                user_to_update.password = request.form['password']
                db.session.commit()
                return redirect('/users')
            except:
                return "There was an error updating the user..."
    else:
            return render_template('update.html' , user_to_update = user_to_update, users = users)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/users')
    except:
      return "There was an error deleting the user..."

##### Custom Error Pages #########

@app.errorhandler(404)
def page_not_found(e):
    return  render_template('404.html'), 404

@app.errorhandler(500)
def page_not_loading(e):
    return  render_template('500.html'), 500

   


    

    
