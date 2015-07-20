# Scott Ouellette
# refineryApp

from flask import Flask, render_template, request, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('app')

app.config.update(
        DEBUG=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///../refineryApp.db',
    )

db = SQLAlchemy(app)

#Blueprint instance created in refineryApp.py
from refineryApp import refineryApp

app.register_blueprint(refineryApp, url_prefix='/refineryApp')
