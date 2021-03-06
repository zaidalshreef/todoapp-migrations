from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,url_for,jsonify,flash,abort,current_app
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:987654321@postgres.cxk76stnikvf.us-east-1.rds.amazonaws.com:5432/todos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except SystemExit:
    db.session.rollback()
    raise 
  finally:
    db.session.close()
  return jsonify({ 'success': True })

@app.route('/todos/<todo_id>/update',methods = ['POST']) 
def update_todos(todo_id):
  try:
   completed = request.get_json()['completed']
   todo = Todo.query.get(todo_id)
   todo.completed = completed
   db.session.commit()
  except SystemExit:
    db.session.rollback()
    raise 
  finally:
    db.session.close
  return redirect(url_for(index))

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except SystemExit:
    error = True
    db.session.rollback()
    raise 
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.order_by('id').all())

if __name__ == '__main__':
    app.run(debug =True)