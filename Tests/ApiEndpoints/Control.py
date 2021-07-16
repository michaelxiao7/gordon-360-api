import pytest
import requests
from urllib.parse import urlsplit, urlunsplit
import pytest_components as api

hostURL = "https://360ApiTrain.gordon.edu/"
#hostURL = "http://localhost:9584/"

FACULTY_PROFILE_IMAGE = "../../Gordon360/Browsable/profile/Test/faculty1.jpg"
STUDENT_PROFILE_IMAGE = "../../Gordon360/Browsable/profile/Test/student1.jpg"
AUTHORIZATION_DENIED = "Authorization has been denied for this request."

searchStr1 = "360"
searchStr2 = "studenttest"

VALID_FACULTY  = "Russ.Tuck"
VALID_FACULTY2 = "Jonathan.Senning"
VALID_STUDENT  = "David.Gurge"
VALID_STUDENT2 = "Elijah.Opoku-Nyarko"

class Control:

    def createGuestSession(self):
        """Create a guest session to test guest calls."""
        return requests.Session()

    def createAuthorizedSession(self, credentials, url):
        """Create an authorized session to test authorized calls."""
        payload = {
            'grant_type':'password',
            'username':credentials.username,
            'password':credentials.password,
        }
        splitURL = urlsplit(url)
        tokenURL = urlunsplit((splitURL.scheme, splitURL.netloc, '/token', '', ''))
        response = requests.post(tokenURL, payload)
        authorization_header = response.json()["token_type"] \
                        + " " + response.json()["access_token"]
        session = requests.Session()
        session.verify = True
        session.headers.update({"Authorization":authorization_header})
        return session

    def getGuestResponse(self, url):
        session = self.createGuestSession()
        return api.get(session, url)

    def getAuthorizedResponse(self, credentials, url):
        """Create an authorized session to test authorized calls."""
        session = self.createAuthorizedSession(credentials, url)
        return api.get(session, url)

    def validate_response(self, response, expected_code=200):
        """Verify HTTP status code matches expected code and response is JSON.

        Args:
            response (requests.models.Response): HTTP response object.
            expected_code (int): expected status code (default is 200 OK).
        """
        if response.status_code != expected_code:
            pytest.fail("Expected status {}, got {}."\
                .format(expected_code, response.status_code))
        try:
            json = response.json()
        except ValueError:
            pytest.fail("Expected JSON response body, got {}.".format(json))
            # or could format response.text
        return json

    def validate_post_response(self, response, expected_code=200):
        """Verify HTTP status code matches expected code and response is JSON.

        Args:
            response (requests.models.Response): HTTP response object.
            expected_code (int): expected status code (default is 200 OK).
        """
        if response.status_code != expected_code:
            pytest.fail("Expected status {}, got {}."\
                .format(expected_code, response.status_code))
