from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import Plan, Expenses
from application.forms import ExpenseForm

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db',
            LIVESERVER_PORT = self.TEST_PORT,
            DEBUG = True,
            TESTING = True
        )
        return app
    
    def setUp(self):
        db.create_all()

        # creating a false plan, to create expenses using this 
        new_plan = Plan(name="Plan 1", budget=1200)
        new_expense = Expenses(plan_id=1, type='Expense 1', expense=1200)
        db.session.add(new_plan)
        db.session.add(new_expense)
        db.session.commit()

        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/update-expense/1')
    
    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
    
    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/update-expense/1')
        assert response.status == 200

class TestAddExpenses(TestBase):
    def submit_input(self, test_case):
        type_field = self.driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[1]/input')
        expense_field = self.driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[2]/input')
        submit = self.driver.find_element_by_xpath('/html/body/div/div/form/div[2]/input')

        type_field.clear()
        type_field.send_keys(test_case[0])
        expense_field.clear()
        expense_field.send_keys(test_case[1])
        submit.click()
    
    def test_update_expense(self):
        test_case = "Update Expenses Type 1", "124.59"
        self.submit_input(test_case)
        assert Expenses.query.filter_by(plan_id=1, type="Update Expenses Type 1", expense=124.59).first() is not None
        assert Expenses.query.filter_by(plan_id=1, type="Expense Type 1", expense=1200).first() is None
        assert Plan.query.filter_by(id=1, name="Plan 1", budget=1200).first() is not None
    
    def test_update_expense_validation(self):
        test_case = " ", "Fail Test"
        self.submit_input(test_case)
        assert Expenses.query.filter_by(plan_id=1, type=" ", expense="Fail Test").first() is None
        assert Expenses.query.filter_by(plan_id=1, type='Expense 1', expense=1200).first() is not None

    def test_add_expense_check_currency_validation(self):
        test_case = "Expense Type Fail", "14.669"
        self.submit_input(test_case)
        
        error = self.driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[2]/div/span')
        assert error.text == 'Please add a currency! (For example 2.99, 12.42)'
        
        assert  Expenses.query.filter_by(type='Expense Type Fail', expense='14.669').first() is None
        assert Expenses.query.filter_by(plan_id=1, type='Expense 1', expense=1200).first() is not None