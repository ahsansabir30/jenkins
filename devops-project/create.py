from application import db
from application.models import *

db.drop_all()
db.create_all()
db.session.commit()

#new_plan = Plan(name="Plan 1", budget=1200)
#new_expense = Expenses(plan_id=1, type='Expense 1', expense=1200)
#db.session.add(new_plan)
#db.session.add(new_expense)
#db.session.commit()