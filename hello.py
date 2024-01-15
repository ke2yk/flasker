from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a secret key for ke2yk"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql//root:gazzo1948@localhost/our_users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gazzo1948@localhost/our_users'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(200), nullable=False)
 email = db.Column(db.String(200), nullable=False, unique=True)
 date_added = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
	return '<Name %r>' % self.name

#FORMS
class UserForm(FlaskForm):
	name = StringField("Name ", validators=[DataRequired()])
	email = EmailField("Email ", validators=[DataRequired(), Email()])
	submit = SubmitField("Submit")	

class NameForm(FlaskForm):
	name = StringField("Name Please", validators=[DataRequired()])
	submit = SubmitField("Submit")

#ROUTES

#INDEX 

#fav_pizza = ["sausage","pepper","pine",55]

#INDEX DISPLAY USERS IF FOUND
@app.route('/')
def index():

	flash("Welcone To Our Website!")

	users = Users.query.order_by(Users.date_added)	

	if users:
		return render_template('index.html',users=users)
	else:
		return render_template('index.html')

#ADD NEW USER
@app.route('/add_user', methods=['GET','POST'])
def add_user():

	name = None
	form = UserForm()

	if form.validate_on_submit():

		user = Users.query.filter_by(email=form.email.data).first()
		
		if user is None:
			user = Users(name=form.name.data, email=form.email.data) 
			db.session.add(user) 
			db.session.commit()
			
			name = form.name.data

			form.name.data = ''
			form.email.data = ''

			flash("User Added Sucessfully!")
		
		else:
		     
		     flash('Email Address Has Already Been Registered')	

	our_users = Users.query.order_by(Users.date_added)	
	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)

#UPDATE USER ID

@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
	
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)

#	if request.method == "POST":

	if form.validate_on_submit():

		name_to_update.name = request.form['name'] 
		name_to_update.email = request.form['email']
	
	try:
		db.session.commit()
		flash("User Updated Successfully")
		return render_template('update.html',form=form, name_to_update=name_to_update)
	
	except:
		flash("User Update Failed Miserably!!!")
		return render_template('update.html',form=form, name_to_update=name_to_update)
	
	else: #Not Post Just Display Form
		return render_template('update.html',form=form, name_to_update=name_to_update)
		
#GET USER NAME
@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

# REQUEST NAME
@app.route('/name', methods=['GET','POST'])
def name():
	
	name = None 
	form = NameForm()
	
	if form.validate_on_submit():
		name = form.name.data 
		form.name.data = ''
		flash("Form Sucessfully Submitted!")

	return render_template('name.html',name=name, form=form)

#ERROR HANDLING
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404


@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500