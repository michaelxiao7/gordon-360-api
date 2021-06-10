import pytest
import warnings
import pytest_components as api
import test_gordon360_pytest as control
from validate import validate_response

class Test_AllAccountTest(control.testCase):
# # # # # # # # #
# ACCOUNT TESTS #
# # # # # # # # #

#    Verify that a user can get account by email
#    Endpoint -- api/accounts/email/{email}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- profile of the email person
    def test_get_user_by_email(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL \
                + 'api/accounts/email/' + control.email + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert response.json()["ADUserName"].lower() \
                            == control.username.lower()
        if "GordonID" in response.json():
            warnings.warn("Security fault, Gordon ID leak")

#    Verify that a user can search by username 
#    Endpoint -- api/accounts/username/{username}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- profile info of {username}
    def test_get_user_by_username(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL \
                + 'api/accounts/username/' + control.leader_username + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert response.json()["ADUserName"].lower() \
                            == control.leader_username.lower()
        if "GordonID" in response.json():
            warnings.warn("Security fault, Gordon ID leak")

#    Verify that a user can search by a single substring of first or last name
#    Endpoint -- api/accounts/search/:searchString
#    Expected Status Code -- 200 OK
#    Expected Response Body -- any info that has the searchString
    def test_search_by_string(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL \
                + 'api/accounts/search/' + control.searchString + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        # Search string should appear in either first or last name of each
        # entry of returned list
        searchString = control.searchString.lower()
        for user in response.json():
            assert (searchString in user["FirstName"].lower() 
                    or searchString in user["LastName"].lower())

#    Verify that a user can search by substrings of both first and last names
#    Endpoint -- api/accounts/search/:searchString1/:searchString2
#    Expected Status Code -- 200 OK
#    Expected Response Body -- any info that has both searchStrings
    def test_search_by_two_strings(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL \
                + 'api/accounts/search/' + control.searchString + '/' \
                                         + control.searchString2 + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert len(response.json()) > 0
        # Search strings should appear in either first and last names
        # of each entry of returned list
        searchString1 = control.searchString.lower()
        searchString2 = control.searchString2.lower()
        for user in response.json():
            assert (searchString1 in user["FirstName"].lower()
                    and searchString2 in user["LastName"].lower())
