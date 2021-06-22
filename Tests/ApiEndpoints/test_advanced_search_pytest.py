import pytest
import warnings
from urllib.parse import urljoin
import pytest_components as api
import Control
import credentials

ROUTE_PREFIX = "api/advanced-search"
SUBROUTES = [
    "majors",
    "minors",
    "halls",
    "states",
    "countries",
    "departments",
    "buildings",
    ]

class Test_AdvancedSearchTest(Control.Control):

# # # # # # # # #
# ADVANCED-SEARCH  TESTS #
# # # # # # # # #

#    Verify that a user can get all advanced-search info.
#    Endpoint -- api/advanced-search/*
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with a list of strings
    def test_get_all_advanced_search_student(self):
        url = "/".join([Control.hostURL, ROUTE_PREFIX])
        session = self.createAuthorizedSession(credentials.student, url)    
        for route in SUBROUTES:
            response = api.get(session, "/".join([url, route]))
            response_json = self.validate_response(response)
            assert type(response_json) is list
            assert len(response_json) > 0
            assert type(response_json[0]) is str
   
#    Verify that a guest user can't get any advanced-search info.
#    Endpoint -- api/advanced-search/*
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied message
    def test_get_all_advanced_search_guest(self):
        url = "/".join([Control.hostURL, ROUTE_PREFIX])
        session = self.createGuestSession()    
        for route in SUBROUTES:
            response = api.get(session, "/".join([url, route]))
            response_json = self.validate_response(response, 401)
            assert response_json['Message'] == Control.AUTHORIZATION_DENIED
