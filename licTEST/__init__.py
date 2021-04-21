from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


app = Flask(__name__)

app.config['SECRET_KEY'] = 'asd'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://yello:A!3a09b86cc@139.162.181.85:3306/licentaDB'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(host='127.0.0.1')

