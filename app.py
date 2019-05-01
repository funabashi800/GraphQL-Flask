from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS

from models import db_session
from schema import schema, Department
from db import db

import os

# Init app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.add_url_rule(
  '/graphql',
  view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True # for having the GraphQL interface
  )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
  db_session.remove()

if __name__ == "__main__":
  db.init_app(app)
  app.run(debug=True)