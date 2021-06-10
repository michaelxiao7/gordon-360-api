import pytest
import warnings
import pytest_components as api
import test_gordon360_pytest as control
from validate import validate_response

class Test_AllDiningTest(control.testCase):
# # # # # # # # #
# DINING  TESTS #
# # # # # # # # #

#    Verify that a student user can get meal plan data.
#    Endpoint -- api/dining/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with dict containing the
#    student mealplan data
    def test_dining_plan_for_student(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL + 'api/dining/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert response.json() == "0"  # Test student should have $0 balance

#    Verify that a faculty user can get meal plan data.
#    Endpoint -- api/dining/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with dict containing the
#    student mealplan data
    def test_dining_plan_for_faculty(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL + 'api/dining/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert response.json() == "0"  # Test faculty should have $0 balance

#    Verify that a guest user can't get meal plan data.
#    Endpoint -- api/dining/
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied message
    def test_dining_plan_for_guest(self):
        self.session = self.createGuestSession()
        self.url = control.hostURL + 'api/dining/'
        response = api.get(self.session, self.url)
        validate_response(response, 401)
        assert response.json()['Message'] == control.AUTHORIZATION_DENIED
