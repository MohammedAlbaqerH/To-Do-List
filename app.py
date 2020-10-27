from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)





class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)




@app.route('/')
def home():
    lists = Todo.query.all()
    return render_template('base.html', lists = lists)


@app.route('/add', methods = ['POST'])
def add():
    title = request.form.get('title')

    new_todo = Todo(title = title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:itm_id>')
def update(itm_id):
    title = request.form.get('title')
    todo = Todo.query.filter_by(id = itm_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:itm_id>')
def delete(itm_id):
    title = request.form.get('title')
    todo = Todo.query.filter_by(id = itm_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    db.create_all()
    app.run(port=6969, debug=True, host="0.0.0.0")