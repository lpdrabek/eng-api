from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

Session = sessionmaker(bind=db_engine)


from app import views, models
