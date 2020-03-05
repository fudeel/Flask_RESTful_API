from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASSWORD@localhost:5432/flaskdb'

# database init
db = SQLAlchemy(app)


# object init on db
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    # define fuction to return a string
    def __repr__(self):
        return '<Task %ds>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['cosa']
        item = Todo(content=content)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return e

    else:
        itemList = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', itemList=itemList)


if __name__ == '__main__':
    app.run(debug=True)
