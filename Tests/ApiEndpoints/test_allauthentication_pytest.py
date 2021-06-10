import pytest
import warnings
import requests
#import string
#from pytest_components import requests
#from datetime import datetime

import pytest_components as api
import test_gordon360_pytest as control
from validate import validate_response

class Test_AllAuthenticationTest(control.testCase):
# # # # # # # # # # # # #
# AUTHENTICATION TESTS  #
# # # # # # # # # # # # #

#    Given valid credentials, verify that authentication is successful for a 
#    student/member.
#    Endpoint -- token/
#    Expected Status code -- 200 Ok
#    Expected Content -- Json Object with access_token attribute.
    def test_authenticate_with_valid_credentials_as_student(self):
        self.session = requests.Session()
        self.url = control.hostURL + 'token'
        self.token_payload = { 'username':control.username, \
            'password':control.password, 'grant_type':'password' }
        response = api.post(self.session, self.url, self.token_payload)
        validate_response(response, 200)
        if 'access_token' not in response.json():
            pytest.fail('Expected access token in response, got {}.'\
                .format(response.json()))
        assert response.json()["token_type"] == "bearer"

#    Given valid credentials, verify that authentication is successful for a 
#    faculty/leader/god.
#    Endpoint --  token/
#    Expected Status code -- 200 Ok
#    Expected Content -- Json Object with access_token attribute.
    def test_authenticate_with_valid_credentials___activity_leader(self):
        self.session = requests.Session()
        self.url = control.hostURL + 'token'
        self.token_payload = { 'username':control.leader_username, \
            'password':control.leader_password, 'grant_type':'password' }
        response = api.post(self.session, self.url, self.token_payload)
        validate_response(response, 200)
        if 'access_token' not in response.json():
            pytest.fail('Expected access token in response, got {}.'\
                .format(response.json()))
        assert response.json()["token_type"] == "bearer"