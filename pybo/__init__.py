from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    app.secret_key = "brokim"

    from .views import main_views, repayment_views, balance_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(repayment_views.bp)
    app.register_blueprint(balance_views.bp)
    
    return app


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8001)))