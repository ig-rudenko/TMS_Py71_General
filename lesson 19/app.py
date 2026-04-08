from flask import Flask

from src.blueprints.main import blueprint as main_blueprint
from src.blueprints.posts import blueprint as posts_blueprint
from src.config import Config
from src.db import db

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(posts_blueprint)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
