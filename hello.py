from flask import Flask, render_template

app = Flask(__name__)

fav_pizza = ["sausage","pepper","pine",55]

@app.route('/')
def index():
	return render_template('index.html',fav_pizza=fav_pizza)


@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404


@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

