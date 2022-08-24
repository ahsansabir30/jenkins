from application import db
from datetime import datetime
from sqlalchemy import false

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=false)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=false)
    
    expenses = db.relationship('Expenses',  cascade="all,delete", backref='plan', lazy=True)

    def __str__(self):
        return str(self.id)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    expense = db.Column(db.Float, nullable=false)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=false)

    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)

    def __str__(self):
        return f"PlanID: {self.plan_id}, Type: {self.type},  Expense: {self.expense}"
