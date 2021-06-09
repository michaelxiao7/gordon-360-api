import pytest
import warnings
#import string
from pytest_components import requests
from datetime import datetime

import pytest_components as api
import test_gordon360_pytest as control

def validate_response(response, expected_code):
    """Verify HTTP status code matches the expected one and response is JSON.

    Args:
        response (requests.models.Response): HTTP response object
        code (int): expected status code
    """
    if response.status_code != expected_code:
        pytest.fail('Expected status {}, got {}.'\
            .format(expected_code, response.status_code))
    try:
        response.json()
    except ValueError:
        pytest.fail('Expected JSON response body, got {}.'\
            .format(response.json()))

def validate_activity(activity):
    """Examine the data returned for a single activity.

    Args:
        activity (str): JSON for a single activity
    
    Verify that the JSON for a single activty has all expected keys,
    that corresponding values have the correct types, and that all required
    values are defined.
    """

    # Verify all expected keys are present and values have expected types
    activityTypes = {
        "ActivityCode":str,
        "ActivityDescription":str,
        "ActivityImagePath":str,
        "ActivityBlurb":str,
        "ActivityURL":str,
        "ActivityType":str,
        "ActivityTypeDescription":str,
        "ActivityJoinInfo":str,
        "Privacy":bool,
    }
    for k in activityTypes.keys():
        assert type(activity[k]) is activityTypes[k]

    # Make sure required values are present
    assert len(activity["ActivityCode"]) > 0
    assert len(activity["ActivityDescription"]) > 0
    assert activity["Privacy"] or not activity["Privacy"]

    # Other sanity checks and warnings
    if len(activity["ActivityURL"]) > 0 \
            and activity["ActivityURL"].find("http") != 0:
        warnings.warn('ActivityURL for {} does not start with "http"'\
            .format(activity["ActivityCode"]))

class Test_AllActivities(control.testCase):
# # # # # # # # # #
# ACTIVITY TESTS  #
# # # # # # # # # #

#    Verify that an activity leader can get all activities.
#    Endpoint -- api/activities/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- List of activities
    def test_get_all_activities___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        if type(response.json()) is not list:
            pytest.fail('Expected list, got {}.'.format(response.json()))

        for activity in response.json():
            validate_activity(activity)

#    Verify that a Guest can get all information for a public activity.
#    Endpoint -- api/activities/360
#    Expected Status Code -- 200 OK
#    Expected Response Body -- List of activities
    def test_get_all_activities___Guest(self):
        self.session = self.createGuestSession()
        self.url = control.hostURL + 'api/activities/' \
            + control.activity_code_360 + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        validate_activity(response.json())
        
#    Verify that an activity leader can get all information for a single
#    activity.
#    Endpoint -- api/activities/{activityCode}
#    Expected Status Code -- 200 OK
#    Expected Response Body - JSON object with activity resource
    def test_get_one_activity___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/' \
             + control.activity_code_AJG + '/'
        response = api.get(self.session, self.url)
        validate_response(response, 200)
        try:
            response.json()['ActivityCode']
        except KeyError:
            pytest.fail('Expected ACT_CDE in response, got {0}.'\
                .format(response.json()))
        assert response.json()["ActivityCode"] == control.activity_code_AJG
        assert response.json()["ActivityDescription"] == \
            control.activity_description_AJG
        assert response.json()["ActivityImagePath"] == \
            control.activity_image_path_AJG
        assert response.json()["ActivityBlurb"] == control.activity_blurb_AJG
        assert response.json()["ActivityURL"] == control.activity_URL_AJG
        assert response.json()["ActivityType"] == control.activity_type_AJG
        assert response.json()["ActivityTypeDescription"] == \
            control.activity_type_description_AJG
        assert response.json()["Privacy"] == True
        assert response.json()["ActivityJoinInfo"] == control.activity_join_info_AJG

#    Verify that an activity leader can get all activities for specific session.
#    Endpoint -- api/activities/session/{sessionCode}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- list of activities
    def test_get_activities_for_session___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/session/201809/'
        response = api.get(self.session, self.url)

        validate_response(response, 200)
        if not (type(response.json()) is list):
            pytest.fail('Expected list, got {0}.'.format(response.json()))
        assert response.json()[1]["ActivityCode"] == control.activity_code_AJG
        assert response.json()[1]["ActivityDescription"] == \
            control.activity_description_AJG
        assert response.json()[1]["ActivityImagePath"] == \
            control.activity_image_path_AJG
        assert response.json()[1]["ActivityBlurb"] == \
            control.activity_blurb_AJG
        assert response.json()[1]["ActivityURL"] == control.activity_URL_AJG
        assert response.json()[1]["ActivityType"] == control.activity_type_AJG
        assert response.json()[1]["ActivityTypeDescription"] == \
            control.activity_type_description_AJG
        assert response.json()[1]["Privacy"] == None
        assert response.json()[1]["ActivityJoinInfo"] == \
            control.activity_join_info_AJG

#    Verify that an activity leader can get all activity types for specific 
#    session in a list 
#    Endpoint -- api/activities/session/{sessionCode}/types
#    Expected Status Code -- 200 OK
#    Expected Response Body -- list of activities
    def test_get_activities_for_session_list___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/session/201809/types/'
        self.sessionID = -1

        response = api.get(self.session, self.url)
        validate_response(response, 200)
        if not (type(response.json()) is list):
            pytest.fail('Expected list, got {0}.'.format(response.json()))
        assert "Student Club" == response.json()[6]
        assert "Scholarship" == response.json()[4]
        assert "Service Learning Project" == response.json()[5]
        assert "Student Ministry" == response.json()[10]
        assert "Athletic Club" == response.json()[0]
        assert "Leadership Program" == response.json()[1]
        assert "Music Group" == response.json()[2]
        assert "Residence Life" == response.json()[3]
        assert "Student Life" == response.json()[8]
        assert "Student Organization" == response.json()[11]
        assert "Theatre Production" == response.json()[12]
        assert "Student Media" == response.json()[9]
        assert "Student Government" == response.json()[7]

#    Verify that an activity leader can get the status of activity in a session 
#    Endpoint -- api/activities/{sessionCode}/{id}/status
#    Expected Status Code -- 200 OK
#    Expected Response Body -- "closed" or "open"
    def test_get_activities_for_session_status___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/' \
            + control.session_code + '/' + control.activity_code_AJG + '/status/'

        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert response.json() == "CLOSED"

#    Verify that an activity leader can get all open status activities
#    Endpoint -- api/activities/open
#    Expected Status Code -- 200 OK
#    Expected Response Body -- a list of open activities
    def test_get_activities_for_session_open___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/open/'

        response = api.get(self.session, self.url)
        validate_response(response, 200)
        assert response.json()[0]["ActivityCode"] == control.activity_code_360
        assert response.json()[0]["ActivityDescription"] == \
            control.activity_description_360
        assert response.json()[0]["ActivityImagePath"] == \
            control.activity_image_path_360
        assert response.json()[0]["ActivityBlurb"] == control.activity_blurb_360
        assert response.json()[0]["ActivityURL"] == control.activity_URL_360

#    Verify that an activity leader can get all closed status activities
#    Endpoint -- api/activities/closed
#    Expected Status Code -- 200 OK
#    Expected Response Body -- "closed" activities
    def test_get_activities_for_session_closed___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/closed/'
        self.sessionID = -1

        response = api.get(self.session, self.url)
        validate_response(response, 200)

#    Verify that an activity leader can get all open status activities per
#    session
#    Endpoint -- api/activities/sessioncode}/open
#    Expected Status Code -- 200 OK
#    Expected Response Body -- activities that are open 
    def test_get_open_activities_for_session___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/201809/open/'
        self.sessionID = -1

        response = api.get(self.session, self.url)
        validate_response(response, 200)

#    Verify that an activity leader can get all closed status activities per 
#    session
#    Endpoint -- api/activities/sessioncode}/closed
#    Expected Status Code -- 200 OK
#    Expected Response Body -- activities that are closed 
    def test_get_closed_activities_for_session___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/' + control.session_code + '/open/'
        self.sessionID = -1

        response = api.get(self.session, self.url)
        validate_response(response, 200)

#    Verify that an activity leader can update activity information.
#    Endpoints -- api/activities/:id
#    Expected Status Code -- 200 Ok
#    Expected Response Body -- Updated activity information
    def test_update_activity___activity_leader(self):
        self.session = \
            self.createAuthorizedSession(control.leader_username, control.leader_password)
        self.url = control.hostURL + 'api/activities/' + control.activity_code_AJG + '/'
        self.data = {
            "ACT_CDE" : control.activity_code_AJG,
            "ACT_BLURB" : control.activity_blurb_AJG,
            "ACT_URL" : control.activity_URL_AJG
        }

        response = api.putAsJson(self.session, self.url , self.data)
        validate_response(response, 200)
        try:
            response.json()['ACT_CDE']
        except ValueError:
            pytest.fail('Expected ACT_CDE in response body, got {0}.'\
                .format(response.json()))