from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import Plan
from application.forms import PlanCreationForm

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
        new_plan = Plan(name="Plan 1", budget=1200)
        db.session.add(new_plan)
        db.session.commit()

        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/update-plan/1')
    
    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
    
    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/update-plan/1')
        assert response.status == 200

class TestAddPlan(TestBase):
    def submit_input(self, test_case):
        name_field = self.driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[1]/input')
        budget_field = self.driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[2]/input')
        submit = self.driver.find_element_by_xpath('/html/body/div/div/form/div[2]/input')

        name_field.clear()
        name_field.send_keys(test_case[0])
        budget_field.clear()
        budget_field.send_keys(test_case[1])
        submit.click()
    
    def test_update_plan(self):
        test_case = "Update Plan 1", "1500.69"
        self.submit_input(test_case)
        assert list(Plan.query.all()) != []
        assert Plan.query.filter_by(name="Update Plan 1").first() is not None
        assert Plan.query.filter_by(name= "Plan 1").first() is None
    
    def test_add_plan_validation(self):
        test_case = "Plan Fail Test", "Not a number"
        self.submit_input(test_case)
        assert Plan.query.filter_by(name="Plan 1").first() is not None
        assert Plan.query.filter_by(name="Plan Fail Test").first() is None
    
    def test_add_plan_check_currency_validation(self):
        test_case = 'Plan Fail Test', '12.499'
        self.submit_input(test_case)
        
        error = self.driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[2]/div/span')
        assert error.text == 'Please add a currency! (For example 2.99, 12.42)'
        
        assert Plan.query.filter_by(name="Plan 1").first() is not None
        assert Plan.query.filter_by(name='Plan Fail Test', budget=12.499).first() is None