import pytest
import warnings
import pytest_components as api
import test_gordon360_pytest as control
#from validate import validate_response

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
        if type(activity[k]) is not activityTypes[k]:
            pytest.fail("Code={} Key={}: Expecting type {} but got type {}"\
                .format(activity["ActivityCode"], k, \
                    activityTypes[k], type(activity[k])))
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
    def test_get_all_activities___leader(self):
        url = control.hostURL + 'api/activities/'
        response = self.getAuthorizedResponse(control.credentials.leader, url)
        response_json = self.validate_response(response)
        if type(response_json) is not list:
            pytest.fail('Expected list, got {}.'.format(response.json()))
        for activity in response_json:
            validate_activity(activity)

#### 2021-06-10 Jonathan Senning
#### The AJG Involvement is private on Train but seems to be public on Prod.
#### Regardless, it seems that this API call does work.  Is this correct?  What
#### does the involvement being private signify?

# #    Verify that a Guest cannot get information for a private activity.
# #    Endpoint -- api/activities/AJG
# #    Expected Status Code -- 404 Not Found
# #    Expected Response Body -- List of activities
#     def test_get_private_activities___Guest(self):
#         self.session = self.createGuestSession()
#         self.url = control.hostURL \
#             + 'api/activities/' + control.activity_code_AJG + '/'
#         response = api.get(self.session, self.url)
#         validate_response(response, 200)
#         validate_activity(response.json())
#         assert response.json()["ActivityCode"] == control.activity_code_AJG
#         assert not response.json()["Privacy"]


#    Verify that a guest can get all information for a public activity.
#    Endpoint -- api/activities/:id
#    Expected Status Code -- 200 OK
#    Expected Response Body -- List of activities
    def test_get_public_activities___guest(self):
        url = control.hostURL + 'api/activities/' + control.activity_code_360 \
                + '/'
        response = api.get(self.createGuestSession(), url)
        response_json = self.validate_response(response)
        validate_activity(response_json)
        assert response_json["ActivityCode"] == control.activity_code_360
        assert not response_json["Privacy"]
        
#    Verify that an activity leader can get all information for a single
#    activity.
#    Endpoint -- api/activities/:id
#    Expected Status Code -- 200 OK
#    Expected Response Body - JSON object with activity resource
    def test_get_one_activity___leader(self):
        url = control.hostURL + 'api/activities/' + control.activity_code_AJG \
                + '/'
        response = self.getAuthorizedResponse(control.credentials.leader, url)
        response_json = self.validate_response(response)
        validate_activity(response_json)
        assert response_json["ActivityCode"] == control.activity_code_AJG
        #assert response_json["Privacy"]

#    Verify that an activity leader can get all activities for specific session.
#    Endpoint -- api/activities/session/{sessionCode}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- list of activities
    def test_get_activities_for_session___leader(self):
        url = control.hostURL + 'api/activities/session/' \
                + control.session_code + '/'
        response = self.getAuthorizedResponse(control.credentials.leader, url)
        response_json = self.validate_response(response)
        if type(response_json) is not list:
            pytest.fail('Expected list, got {}.'.format(response_json))
        for activity in response_json:
            validate_activity(activity)

#    Verify that an activity leader can get all activity types for specific 
#    session in a list 
#    Endpoint -- api/activities/session/{sessionCode}/types
#    Expected Status Code -- 200 OK
#    Expected Response Body -- list of activities
    def test_get_activities_for_session_list___leader(self):
        url = control.hostURL + 'api/activities/session/' \
                + control.session_code + '/types/'
        response = self.getAuthorizedResponse(control.credentials.leader, url)
        response_json = self.validate_response(response)
        if type(response_json) is not list:
            pytest.fail('Expected list, got {}.'.format(response.json()))
        # Be sure the list of types is not empty and each entry is
        # a nonempty string
        assert len(response_json) > 0
        for activity_type in response_json:
            assert type(activity_type) is str and len(activity_type) > 0

#    Verify that an activity leader can get the status of activity in a session 
#    Endpoint -- api/activities/{sessionCode}/{id}/status
#    Expected Status Code -- 200 OK
#    Expected Response Body -- "closed" or "open"
    def test_get_activities_for_session_status___leader(self):
        url = control.hostURL + 'api/activities/' + control.session_code \
                + '/' + control.activity_code_AJG + '/status/'
        response = self.getAuthorizedResponse(control.credentials.leader, url)
        response_json = self.validate_response(response)
        assert response_json == "CLOSED"

#    Verify that an activity leader can get all open status activities
#    Endpoint -- api/activities/open
#    Expected Status Code -- 200 OK
#    Expected Response Body -- a list of open activities
    def test_get_activities_for_session_open___leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
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
    def test_get_activities_for_session_closed___leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL + 'api/activities/closed/'
        #self.sessionID = -1
        response = api.get(self.session, self.url)
        validate_response(response, 200)

#    Verify that an activity leader can get all open status activities per
#    session
#    Endpoint -- api/activities/sessioncode}/open
#    Expected Status Code -- 200 OK
#    Expected Response Body -- activities that are open 
    def test_get_open_activities_for_session___leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL + 'api/activities/201809/open/'
        #self.sessionID = -1
        response = api.get(self.session, self.url)
        validate_response(response, 200)

#    Verify that an activity leader can get all closed status activities per 
#    session
#    Endpoint -- api/activities/sessioncode}/closed
#    Expected Status Code -- 200 OK
#    Expected Response Body -- activities that are closed 
    def test_get_closed_activities_for_session___leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL + 'api/activities/' \
                                    + control.session_code + '/open/'
        #self.sessionID = -1
        response = api.get(self.session, self.url)
        validate_response(response, 200)

#    Verify that an activity leader can update activity information.
#    Endpoints -- api/activities/:id
#    Expected Status Code -- 200 Ok
#    Expected Response Body -- Updated activity information
    def test_update_activity___leader(self):
        self.session = self.createAuthorizedSession(control.leader_username, \
                                control.leader_password)
        self.url = control.hostURL + 'api/activities/' \
                                    + control.activity_code_AJG + '/'
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
