from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    from .views import main_views, repayment_views, balance_views, graph_views

    app.register_blueprint(main_views.bp)
    app.register_blueprint(repayment_views.bp)
    app.register_blueprint(balance_views.bp)
    app.register_blueprint(graph_views.bp)
    
    # 필터
    from .filter import format_datetime,number_format_simple,ratio_to_percent_format
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['number_format_simple'] = number_format_simple
    app.jinja_env.filters['ratio_to_percent_format'] = ratio_to_percent_format

    return app


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8001)))
