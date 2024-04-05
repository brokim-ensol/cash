from pybo import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped

db: SQLAlchemy


class Repayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    modified_at = db.Column(db.Date, nullable=True)
    remark = db.Column(db.String(200), nullable=True)


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repayment_id = db.Column(db.Integer, db.ForeignKey("repayment.id"))
    repayment: Mapped["Repayment"] = db.relationship(
        "Repayment", backref=db.backref("balance", uselist=False)
    )
    balance = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(200), nullable=True)
    repaid_dt = db.Column(db.Date, nullable=False)
    ratio = db.Column(db.Float, nullable=True)
