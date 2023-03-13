from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SqlAlchemy Database Configuration With Mysql
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

app.app_context().push()

#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(300))
    is_completed = db.Column(db.Boolean)
 
    def __init__(self, todo):
        self.todo = todo
        self.is_completed = False

@app.route('/add', methods=['POST'])
def add_todo():
	# db.session.add_all([obj1, obj2])
	todo_f = request.form["todo"]
	obj = Data(todo_f)
	db.session.add(obj)
	# db.session.add(Data(request.form["todo"], False))
	db.session.commit()

	flash('Todo added successfully!!', 'success')
	return redirect(url_for('home'))

@app.route('/edit', methods=['POST'])
def edit_todo():
	id_m = request.form["todo_id_m"]
	todo_m = request.form["todo_m"]
	
	todo_c = Data.query.get(id_m)
	todo_c.todo = todo_m
	db.session.commit()
	flash('Todo modified successfully!!', 'success')
	return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete_todo(id):
	row = Data.query.get(id)
	db.session.delete(row)
	db.session.commit()
	flash('Todo successfully deleted!!', 'success')
	return redirect(url_for('home'))

@app.route('/completed/<id>')
def complete_todo(id):
	todo = Data.query.get(id)
	todo.is_completed = True
	db.session.commit()
	flash(f'{todo.todo} is completed!!', 'success')
	return redirect(url_for('home'))

@app.route('/notcompleted/<id>')
def not_complete_todo(id):
	todo = Data.query.get(id)
	todo.is_completed = False
	db.session.commit()
	return redirect(url_for('home'))

@app.route('/filter/<int:num>')
def filter_todo(num):
	if num == 1:
		return redirect(url_for('home'))
	elif num == 2:
		todos = Data.query.filter_by(is_completed = False)
		return render_template('home.html', todos = todos)
	elif num == 3:
		todos = Data.query.filter_by(is_completed = True)
		return render_template('home.html', todos = todos)

@app.route('/')
def home():
	todos = Data.query.all()
	return render_template('home.html', todos = todos)

if __name__ == '__main__':
	# create_database(app)
	db.create_all()
	app.run(debug=True)