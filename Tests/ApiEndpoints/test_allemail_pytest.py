import pytest
import warnings
import pytest_components as api
import test_gordon360_pytest as control
from validate import validate_response

def validate_users(users):
    """Examine the data (names and emails) returned for a single activity.

    Args:
        users (list): List of dictionaries with FirstName, LastName, and
                        Email entries.
    
    Verify that the dictionaries in the users list each have the keys
    FirstName, LastName, and Email and that corresponding values are
    nonempty strings.
    """
    if type(users) is not list:
        pytest.fail('Expected list, got {}.'.format(users))
    for user in users:
        for k in ["FirstName", "LastName", "Email"]:
            assert type(user[k]) == str and len(user[k]) > 0

class Test_AllEmailTest(control.testCase):
# # # # # # # #
# EMAIL TEST  #
# # # # # # # #

#    Verify that a student member can get a list of the emails for all members 
#    in the activity.
#    Endpoint -- api/emails/activity/{activity_ID}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A JSON response with the student resource
    def test_get_list_of_emails(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL \
            + 'api/emails/activity/' + control.activity_code_360 + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_users(response.json())

#   Verify that an activity leader can get the emails for the members of an 
#   activity in specific session code 
#   Endpoint -- api/emails/activity/:id/session/:sessionid
#   Expected Status Code -- 200 OK
#   Expected Response Body -- A JSON robjects
    def test_get_emails_for_activity___activity_leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL \
            + 'api/emails/activity/' + control.activity_code_AJG \
            + '/session/' + control.session_code + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_users(response.json())

#    Verify that a supervisor can get the emails for any activity leader based 
#    on a session code
#    Endpoint -- api/emails/activity/:id/leaders/session/:sessionCode
#    Expected Status Code -- 200 OK
#    Expected Response Body -- Json response with a list of emails
    def test_get_emails_for_leaders___supervisor(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL \
            + 'api/emails/activity/' + control.activity_code_AJG \
            + '/leaders/session/' + control.session_code + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_users(response.json())
        #assert response.json()[0]['Email'] == "Emmy.Short@gordon.edu"
        #assert response.json()[0]['FirstName'] == "Emmy"
        #assert response.json()[0]['LastName'] == "Short"

#    Verify that a leader can get the advisor for a student's involvement based
#    on activity code and session code.
#    Endpoint -- api/emails/activity/AJG/advisors/session/201809
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with the student resource
    def test_get_student_by_email___advisor(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL \
            + 'api/emails/activity/' + control.activity_code_AJG \
            + '/advisors/session/' + control.session_code + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_users(response.json())
        #assert response.json()[0]['Email'] == "Chris.Carlson@gordon.edu"
        #assert response.json()[0]['FirstName'] == "Christopher"
        #assert response.json()[0]['LastName'] == "Carlson"

#    Verify that a supervisor can get the emails for any advisor
#    Endpoint -- api/emails/activity/:id/advisor
#    Expected Status Code -- 200 OK
#    Expected Response Body -- Json response with a list of emails
    def test_get_all_advisor_emails___supervisor(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL \
            + 'api/emails/activity/' + control.activity_code_360 + '/advisors/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_users(response.json())
        #assert response.json()[0]['Email'] == "Chris.Carlson@gordon.edu"
        #assert response.json()[0]['FirstName'] == "Christopher"
        #assert response.json()[0]['LastName'] == "Carlson"

#    Verify that a supervisor can get the emails for any advisors based on 
#    session code
#    Endpoint -- api/emails/activity/:id/advisors/session/{sessioncode}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- Json response with a list of emails
    def test_get_emails_for_group_admin___supervisor(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL \
            + 'api/emails/activity/' + control.activity_code_AJG \
            + '/advisors/session/' + control.session_code + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_users(response.json())
        #assert response.json()[0]['Email'] == "Chris.Carlson@gordon.edu"
        #assert response.json()[0]['FirstName'] == "Christopher"
        #assert response.json()[0]['LastName'] == "Carlson"

#    Verify that a 404 Not Found error message will be returned based on a
#    bad session code
#    Precondition -- Shouldn't return anything if activity id isn't valid
#    Endpoint -- api/emails/activity/:id
#    Expected Status Code -- 404 Not Found
#    Expected Response Body -- Not Found error message
    #@pytest.mark.skipif(not control.unknownPrecondition, reason = "Shouldn't allow access"\
    #    " because the activity id doesn't exist")
    def test_get_emails_for_nonexistant_activity___leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL + 'api/emails/activity/DoesNotExist'
        response = api.get(self.session, self.url)
        validate_response(response, 404)

#    Verify that a 401 Unauthorized error message will be returned to
#    a member when attempting to access a nonexistant activity
#    Precondition -- Shouldn't return anything if activity id isn't valid
#    Endpoint -- api/emails/activity/:id
#    Expected Status Code -- 401 Unauthorized
#    Expected Response Body -- Not Found error message
    def test_get_emails_for_nonexistant_activity___member(self):
        self.session = self.createAuthorizedSession(control.username, \
                                control.password)
        self.url = control.hostURL + 'api/emails/activity/DoesNotExist'
        response = api.get(self.session, self.url)
        validate_response(response, 401)
