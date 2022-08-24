from application import app, db
from flask import render_template, url_for, flash, redirect, request
from application.forms import PlanCreationForm, ExpenseForm
from application.models import Plan, Expenses

@app.route("/")
def plan_view():
    plans = Plan.query.all()
    return render_template('planner.html', plans=plans)

@app.route("/new-plan", methods=['GET', 'POST'])
def create_plan():
    header = "Create New Plan"
    form = PlanCreationForm()
    if form.validate_on_submit():
        new_plan = Plan(name=form.name.data, budget=form.budget.data)
        db.session.add(new_plan)
        db.session.commit()
        flash(f"Plan was created successfully {form.name.data}!", 'success')
        return redirect(url_for('plan_view'))

    return render_template('planform.html', form=form, header=header)

@app.route("/update-plan/<int:plan_id>", methods=['GET', 'POST'])
def update_plan(plan_id):
    # need to query database first
    plan = Plan.query.get_or_404(plan_id)
    form = PlanCreationForm()

    if form.validate_on_submit():
        plan.name = form.name.data
        plan.budget = form.budget.data
        db.session.commit()
        flash(f"Plan was updated successfully!", 'success')
        return redirect(url_for('plan_view'))
    elif request.method == 'GET':
        # loading form data
        form.name.data = plan.name
        form.budget.data = plan.budget

    header = f"Update Plan: {plan.name}"
    return render_template('planform.html', plan=plan, form=form, header=header)

@app.route("/delete-plan/<int:plan_id>/", methods=['GET', 'POST'])
def delete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('plan_view'))

@app.route("/expenses/<int:plan_id>")
def plan_expense(plan_id):
    plan =  Plan.query.get_or_404(plan_id)

    total_expenses = 0
    for expense in plan.expenses:
        total_expenses = total_expenses + expense.expense
        
    return render_template('expenses.html', plan=plan, total_expenses=total_expenses)

@app.route("/new-expense/<int:plan_id>", methods=['GET', 'POST'])
def create_expense(plan_id):
    plan = Plan.query.get_or_404(plan_id)

    header = f"{plan.name}: New Expense"

    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expenses(plan=plan, type=form.type.data, expense=form.expense.data)
        db.session.add(new_expense)
        db.session.commit()
        flash(f"{form.type.data} expense was created successfully!", 'success')
        return redirect(url_for('plan_expense', plan_id=plan_id))

    return render_template('expenseform.html', form=form, plan_id=plan.id, header=header)

@app.route("/update-expense/<int:expense_id>", methods=['GET', 'POST'])
def update_expense(expense_id):
    # need to query datsabase first
    expense = Expenses.query.get_or_404(expense_id)
    
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.type = form.type.data
        expense.expense = form.expense.data
        db.session.commit()
        flash(f"{expense.type} expense was updated successfully!", 'success')
        return redirect(url_for('plan_expense', plan_id=expense.plan_id))
    elif request.method == 'GET':
        # loading form data
        form.type.data = expense.type
        form.expense.data = expense.expense

    header = f"Update Expense: {expense.type}"
    plan_id = expense.plan_id
    return render_template('expenseform.html', form=form, header=header, expense=expense, plan_id=plan_id)

@app.route("/delete-expense/<int:expense_id>", methods=['GET', 'POST'])
def delete_expense(expense_id):
    expense = Expenses.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash(f'Your {expense.type} expense has been deleted!', 'success')
    return redirect(url_for('plan_expense', plan_id=expense.plan_id))