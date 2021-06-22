import pytest
import warnings
from urllib.parse import urljoin
import pytest_components as api
import Control
import credentials

ROUTE_PREFIX = "api/dining"

class Test_AllDiningTest(Control.Control):

# # # # # # # # #
# DINING  TESTS #
# # # # # # # # #

#    Verify that a student user can get meal plan data.
#    Endpoint -- api/dining/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with dict containing the
#    student mealplan data
    def test_dining_plan_for_student(self):
        url = urljoin(Control.hostURL, ROUTE_PREFIX)
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        assert response_json == "0"  # Test student should have $0 balance

#    Verify that a faculty user can get meal plan data.
#    Endpoint -- api/dining/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with dict containing the
#    student mealplan data
    def test_dining_plan_for_faculty(self):
        url = urljoin(Control.hostURL, ROUTE_PREFIX)
        response = self.getAuthorizedResponse(credentials.faculty, url)
        response_json = self.validate_response(response)
        assert response_json == "0"  # Test faculty should have $0 balance

#    Verify that a guest user can't get meal plan data.
#    Endpoint -- api/dining/
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied message
    def test_dining_plan_for_guest(self):
        url = urljoin(Control.hostURL, ROUTE_PREFIX)
        response = self.getGuestResponse(url)
        response_json = self.validate_response(response, 401)
        assert response_json['Message'] == Control.AUTHORIZATION_DENIED
