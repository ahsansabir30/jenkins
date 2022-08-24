from flask import url_for
from application import app, db
from flask_testing import TestCase
from application.models import Plan, Expenses

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
            DEBUG=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY = 'NADSKJADSNJDA54DSAJKNDAJ4'
        )
        return app
        
    def setUp(self):
        # creating test object in the database
        db.create_all()
        # creating a fake plan
        new_plan = Plan(name="Plan 1", budget=1200)
        new_expense = Expenses(plan_id=1, type='Expense 1', expense=1200)
        db.session.add(new_plan)
        db.session.add(new_expense)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    # Testing Plan Views
    def test_get_plan(self):
        response = self.client.get(url_for('plan_view'))
        self.assert200(response)
        self.assertIn(b'Plan 1', response.data)

    def test_get_create_plan(self):
        response = self.client.get(url_for('create_plan'))
        self.assert200(response)
        self.assertIn(b'Create New Plan', response.data)


    def test_get_update_plan(self):
        response = self.client.get(url_for('update_plan', plan_id=1))
        self.assert200(response)
        self.assertIn(b'Plan 1', response.data)


    def test_get_delete_plan(self):
        response = self.client.get(url_for('delete_plan', plan_id=1), follow_redirects=True)
        self.assert200(response)
        self.assertNotIn(b'Plan 1', response.data)

        # if we delete a plan - all the expense related to that plan should also be deleted
        assert Plan.query.filter_by(id=1).first() is None
        assert Expenses.query.filter_by(plan_id=1).first() is None

    # Testing Expense Views
    def test_get_expense_view(self):
        response = self.client.get(url_for('plan_expense', plan_id=1))
        self.assert200(response)
        self.assertIn(b'Plan 1', response.data)


    def test_get_create_expense(self):
        response = self.client.get(url_for('create_expense', plan_id=1))
        self.assert200(response)
        self.assertIn(b'Plan 1: New Expense', response.data)


    def test_get_update_expense(self):
        response = self.client.get(url_for('update_expense', expense_id=1))
        self.assert200(response)
        self.assertIn(b'Expense 1', response.data)


    def test_get_delete_expense(self):
        response = self.client.get(url_for('delete_expense', expense_id=1), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Your Expense 1 expense has been deleted!', response.data)

        assert Expenses.query.filter_by(id=1).first() is None

class TestPostRequest(TestBase):
    # Test Post Request for Plan
    def test_add_plan(self):
        response = self.client.post(
            url_for('create_plan'),
            data = dict(name="Plan 2", budget=1000),
            follow_redirects = True
        )
        
        self.assert200(response)
        self.assertIn(b'Plan 2', response.data)
        # we also can check the database directly
        assert Plan.query.filter_by(name='Plan 2').first() is not None

    def test_update_plan(self):
        response = self.client.post(
            url_for('update_plan', plan_id=1),
            data = dict(name="Update Plan 1", budget=1400),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Update Plan 1', response.data)

        assert Plan.query.filter_by(name='Update Plan 1').first() is not None
        assert Plan.query.filter_by(name='Plan 1').first() is None

    # Test Post Request for Expenses
    def test_add_expense(self):
        response = self.client.post(
            url_for('create_expense', plan_id=1),
            data = dict(type="Expense 2", expense=1000),
            follow_redirects = True
        )
        
        self.assert200(response)
        self.assertIn(b'Expense 2', response.data)
        
        # checking if the add expense has been created under the given plan id
        assert Expenses.query.filter_by(plan_id=1, type='Expense 2').first() is not None


    def test_update_expense(self):
        response = self.client.post(
            url_for('update_expense', expense_id=1),
            data = dict(type="Update Expense 1", expense=1200),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Update Expense 1', response.data)

        assert Expenses.query.filter_by(plan_id=1, type='Update Expense 1').first() is not None
        assert Expenses.query.filter_by(type='Expense 1').first() is None