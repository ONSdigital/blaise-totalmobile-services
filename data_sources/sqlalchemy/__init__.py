from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data_sources/sqlalchemy/temp.db'
db = SQLAlchemy(app)
db.create_all()
