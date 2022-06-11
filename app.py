#Flask, render_template, request, redirect, flash
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = "admin12345"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

# Initilize the database
db = SQLAlchemy(app)

#### Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    e_mail =  EmailField('E-mail', validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField('Submit')


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


@app.route('/users', methods =['POST', 'GET'])
def users():
        
    name = None
    e_mail = None
    password = None
    form = UserForm()

    # Validate Form
    if form.validate_on_submit():
        flash("User added sucessfully!")
        name = form.name.data
        form.name.data = ''
        e_mail = form.e_mail.data
        form.e_mail.data = ''
        password = form.password.data
        form.password.data = ''
        
        users = Users.query.order_by(Users.date_created)

        new_user = Users(name= name, e_mail = e_mail, password = password )
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
        return render_template('users.html', users = users, form = form) 


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    
    users = Users.query.order_by(Users.date_created)
    form = UserForm()

    # Validate Form
    if form.validate_on_submit():
        flash("User added sucessfully!")
        name = form.name.data
        form.name.data = ''
        e_mail = form.e_mail.data
        form.e_mail.data = ''
        password = form.password.data
        form.password.data = ''
    # push to database
        try:
            
            user_to_update = Users.query.get_or_404(id)
            user_to_update = Users.query.get(user_to_update)
            user_to_update.name = name
            user_to_update.e_mail = e_mail
            user_to_update.password = password
            db.session.commit()
            return redirect('/users')
        except:
                return "There was an error adding the user..."
        return "you clicked the button"
    else:
        return render_template('update.html' , users = users, form = form)

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
    return  render_template('400.html'), 500



   


    

    
