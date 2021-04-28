import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

connex_app = connexion.App(__name__, specification_dir="./openapi/")
app = connex_app.app

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:mysql@192.168.10.175/petstore'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
db.metadata.clear()
ma = Marshmallow(app)
