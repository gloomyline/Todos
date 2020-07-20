import os, click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False) == 'True'

db = SQLAlchemy(app)

class Note(db.Model):
  """Note model class"""
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)

  def __repr__(self):
    return '<Note %r>' % self.body

class Author(db.Model):
  """Author model class"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(70), unique=True)
  phone = db.Column(db.String(20), unique=True)
  articles = db.relationship('Article')

class Article(db.Model):
  """Article model class"""
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), unique=True)
  body = db.Column(db.Text)
  author_id = db.Column(db.Integer, db.ForeignKey('%s.id' % Author.__tablename__))
    
@app.cli.command()
def initdb():
  """Initialize database."""
  db.create_all()
  click.echo('Initialized database.')

@app.shell_context_processor
def make_shell_context():
  return dict(db=db, Note=Note, Author=Author, Article=Article)