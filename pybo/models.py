from pybo import db
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy

class Repayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=True)
    remark = db.Column(db.String(200), nullable=True)
    
class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repayment_id = db.Column(db.Integer, db.ForeignKey('repayment.id', ondelete='CASCADE'))
    repayment = db.relationship('Repayment', backref=db.backref('balance_set', cascade='all, delete-orphan'))
    balance = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(200), nullable=True)
    ratio = db.Column(db.Float, nullable=False)