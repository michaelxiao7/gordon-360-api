import pytest
import warnings
#import string
#from pytest_components import requests
#from datetime import datetime

#import base64
import Control
import pytest_components as api
import pytest_credentials as credentials
#import test_gordon360_pytest as control

ROUTE_PREFIX = "/".join([Control.hostURL, "api/profiles"])

class Test_AllProfileTest(Control.Control):
#################
# PROFILE TESTS #
#################

#    Verify that a user can get their own profile
#    Endpoint -- api/profiles/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json object of information on own profile
    def test_get_my_profile(self):
        url = "/".join([ROUTE_PREFIX, "/"])
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        try:
            assert response_json['AD_Username'].lower() \
                        == credentials.student.getUsername().lower()
            assert int(response_json['ID']) == credentials.student.getID()
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that guests cannot get their own profile
#    Endpoint -- api/profiles/
#    Expected Status Code -- 401 Authorization Error
#    Expected Response Body -- An authorization denied message
    def test_get_guest_my_profile(self):
        url = "/".join([ROUTE_PREFIX, "/"])
        response = self.getGuestResponse(url)
        response_json = self.validate_response(response, 401)
        try:
            assert response_json['Message'] == Control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that a user can get another person's profile, filtering
#    private information
#    Endpoint -- api/profiles/{username}
#    Expected Status Code -- 200 Ok
#    Expected Response Body -- list of information on the user without private
#    info
    def test_get_profile_by_username(self):
        username = credentials.faculty.getUsername()
        url = "/".join([ROUTE_PREFIX, username, "/"])
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        try:
            assert response_json['AD_Username'].lower() == username.lower()
            assert "ID" not in response.json()
        except ValueError:
            pytest.fail('Expected Json response body, got{}.'\
                .format(response.text))

#    Verify that a guest can't get another person's profile
#    Endpoint -- api/profiles/:username
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied message
    def test_get_guest_profile_by_username(self):
        username = credentials.student.getUsername()
        url = "/".join([ROUTE_PREFIX, username, "/"])
        response = self.getGuestResponse(url)
        response_json = self.validate_response(response, 401)
        try:
            assert response_json['Message'] == Control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that a user can get a profile image of the current user
#    Endpoint -- api/profiles/image
#    Expected Status Code -- 200 Ok
#    Expected Response Body -- image path of the current user
    def test_get_image(self):
        url = "/".join([ROUTE_PREFIX, "image", "/"])
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        try:
            key = list(response_json.keys())[0]
            assert key == "def" or key == "pref"
            assert len(response_json[key]) > 0
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that a guest can't get a profile image of the current user
#    Endpoint -- api/profiles/image
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied message
    def test_get_guest_image(self):
        url = "/".join([ROUTE_PREFIX, "image", "/"])
        response = self.getGuestResponse(url)
        response_json = self.validate_response(response, 401)
        try:
            assert response_json['Message'] == Control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that a user can get a profile image of someone else
#    Endpoint -- api/profiles/image/{username}
#    Expected Status Code -- 200 Ok
#    Expected Response Body -- image path of another user
    def test_get_image_by_username(self):
        username = credentials.faculty.getUsername()
        url = "/".join([ROUTE_PREFIX, "image", username, "/"])
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        try:
            key = list(response_json.keys())[0]
            assert key == "def" or key == "pref"
            assert len(response_json[key]) > 0
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that a guest can't get a profile image of someone else
#    Endpoint -- api/profiles/image/:username
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied message
    def test_get_guest_image_by_username(self):
        username = credentials.student.getUsername()
        url = "/".join([ROUTE_PREFIX, "image", username, "/"])
        response = self.getGuestResponse(url)
        response_json = self.validate_response(response, 401)
        try:
            assert response_json['Message'] == Control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got {}.'\
                .format(response.text))

#    Verify that a user can upload a profile image
#    Endpoint -- api/profiles/image/
#    Expected Status Code -- 200 OK
#    Expected Content -- updated profile image
    def test_post_profile_image(self):
        url = "/".join([ROUTE_PREFIX, "image", "/"])
        session = self.createAuthorizedSession(credentials.faculty, url)

        data = {
            'pref': open(Control.FACULTY_PROFILE_IMAGE, 'rb')
        }        
        response = api.postAsFormData(session, url, data)
        self.validate_post_response(response)
        #self.data = {
        #    'ID': my_id_number,
        #    'FILE_PATH': FILE_PATH,
        #    'FILE_NAME': FILE_NAME
        #}
#        d = api.post(self.session, self.url + 'reset/', self.data)
#        if not d.status_code == 200:
#            pytest.fail('There was a problem performing cleanup')

#    Verify that a user can reset a profile image
#    Endpoint -- api/profiles/image/reset/
#    Expected Status Code -- 200 OK
#    Expected Content --
    def test_post_reset_image(self):
        url = "/".join([ROUTE_PREFIX, "image", "reset", "/"])
        session = self.createAuthorizedSession(credentials.faculty, url)
        data = {}
        #self.requestID = -1
        response = api.post(session, url, {})
        self.validate_post_response(response)

"""
#    Verify that a guest cannot upload a profile image
#    Endpoint -- api/profiles/image/
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Content -- An authorization denied message
    def test_post_guest_profile_image(self):
        self.session = self.createGuestSession()
        self.url = control.hostURL + 'api/profiles/image/'
        self.data = {
            'file': open(control.FILE_PATH_PROFILE, 'r')
        }

        response = api.postAsFormData(self.session, self.url, self.data)
        print(response.json())
        if not response.status_code == 401:
            pytest.fail('Expected 401 Unauthorized Error, got {0}.'\
                .format(response.status_code))
        try:
            assert response.json()['Message'] == control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got{0}.'\
                .format(response.text))

#    Verify that a user can upload an ID image
#    Pre-conditions -- unknown
#    Endpoint -- api/profiles/IDimage/
#    Expected Status Code -- 200 OK
#    Expected Content -- upload ID photo
    @pytest.mark.skipif(not control.unknownPrecondition, reason = \
        "Unknown reason for error")
    def test_post_ID_image(self):
        self.session = self.createAuthorizedSession(control.username, control.password)
        self.url = control.hostURL + 'api/profiles/IDimage/'
        self.data = {
            'file': open(control.FILE_PATH_ID, 'r')
        }
        
        response = api.postAsFormData(self.session, self.url, self.data)
        if not response.status_code == 200:
            pytest.fail('Expected 200 OK, got {0}.'\
                .format(response.status_code))
            
        d = api.post(self.session, self.url + 'reset/', self.data)
        if not d.status_code == 200:
            pytest.fail('There was a problem performing cleanup')

#    Verify that a guest can't upload an ID image
#    Endpoint -- api/profiles/IDimage/
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Content -- An authorization denied message
    def test_post_guest_ID_image(self):
        self.session = self.createGuestSession()
        self.url = control.hostURL + 'api/profiles/IDimage/'
        self.data = {
            'file': open(control.FILE_PATH_ID, 'r')
        }
        response = api.postAsFormData(self.session, self.url, self.data)
        if not response.status_code == 401:
            pytest.fail('Expected 401 OK, got {0}.'\
                .format(response.status_code))
        try:
            assert response.json()['Message'] == control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got{0}.'\
                .format(response.text))

#    Verify that a guest can't reset a profile image
#    Endpoint -- api/profiles/image/reset/
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Content -- An authorization denied message
    def test_post_guest_reset_image(self):
        self.session = self.createGuestSession()
        self.url = control.hostURL + 'api/profiles/image/reset/'
        self.data = {
            'ID': control.my_id_number,
            'FILE_PATH': control.FILE_PATH_PROFILE,
            'FILE_NAME': ""
        }
        self.requestID = -1
        response = api.post(self.session, self.url, self.data)
        if not response.status_code == 401:
            pytest.fail('Expected 401 Created, got {0}.'\
                .format(response.status_code))
        try:
            assert response.json()['Message'] == control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got{0}.'\
                .format(response.text))

#    Verify that a user can add and edit social media links
#    Endpoint -- api/profiles/:type
#    Expected Status Code -- 200 OK
#    Expected Content --
    def test_put_social_media_links(self):
        self.session = self.createAuthorizedSession(control.username, control.password)
        self.url = control.hostURL + 'api/profiles/facebook/'
        self.data = {
            'facebook': 'https://www.facebook.com/360.studenttest' 
            #'URL of any SNS including the domain name'
        }
        response = api.put(self.session, self.url, self.data)
        if not response.status_code == 200:
            pytest.fail('Expected 200 OK, got {0}.'\
                .format(response.status_code))
        self.resetdata = {
            'facebook': 'Changed for testing'
        }
        d = api.put(self.session, self.url, self.resetdata)
        if not d.status_code == 200:
            pytest.fail('There was a problem performing cleanup')

#    Verify that a guest can't add and edit social media links
#    Endpoint -- api/profiles/:type
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Content -- An authorization denied message
    def test_put_guest_social_media_links(self):
        self.session = self.createGuestSession()
        self.url = control.hostURL + 'api/profiles/facebook/'
        self.data = {
            'facebook': 'https://www.facebook.com/360.studenttest'
        }
        response = api.put(self.session, self.url, self.data)
        if not response.status_code == 401:
            pytest.fail('Expected 401 OK, got {0}.'\
                .format(response.status_code))
        try:
            assert response.json()['Message'] == control.AUTHORIZATION_DENIED
        except ValueError:
            pytest.fail('Expected Json response body, got{0}.'\
                .format(response.text))
            

#    Verify that a user can turn on and off mobile privacy
#    Endpoint -- api/profiles/mobile_privacy/:value (Y or N)
#    Expected Status Code -- 200 OK
#    Expected Content -- Make mobile privacy 0 or 1
    def test_put_mobile_privacy(self):
        self.session = self.createAuthorizedSession(control.username, control.password)
        self.url = control.hostURL + 'api/profiles/mobile_privacy/Y/'
        self.data = {
            'IsMobilePhonePrivate': 'Y'
        }
        response = api.put(self.session, self.url, self.data)
        if not response.status_code == 200:
            pytest.fail('Expected 200 OK, got {0}.'\
                .format(response.status_code))
        profile_url = control.hostURL + 'api/profiles/'
        check_response = api.get(self.session,profile_url)
        assert check_response.json()['IsMobilePhonePrivate'] == 1
        self.url = control.hostURL + 'api/profiles/mobile_privacy/N/'
        self.resetdata = {
            'IsMobilePhonePrivate': 'N'
        }
        d = api.put(self.session, self.url, self.resetdata)
        if not d.status_code == 200:
            pytest.fail('There was a problem performing cleanup')
        check_response = api.get(self.session,profile_url)
        assert check_response.json()['IsMobilePhonePrivate'] == 0

#    Verify that a user can edit image privacy
#    Endpoint -- api/profiles/image_privacy/:value (Y or N) 
#    Expected Status Code -- 200 OK 
#    Expected Content -- 
    def test_put_image_privacy(self): 
        self.session = self.createAuthorizedSession(control.username, control.password) 
        self.url = control.hostURL + 'api/profiles/image_privacy/Y/' 
        self.data = { 
            'show_pic': 'Y' 
        } 
        response = api.put(self.session, self.url, self.data) 
        if not response.status_code == 200: 
            pytest.fail('Expected 200 OK, got {0}.'\
                .format(response.status_code)) 
        profile_url = control.hostURL + 'api/profiles/' 
        check_response = api.get(self.session,profile_url) 
        assert check_response.json()['show_pic'] == 1 
        self.url = control.hostURL + 'api/profiles/image_privacy/N/' 
        self.resetdata = { 
            'show_pic': 'N' 
        } 
        d = api.put(self.session, self.url, self.resetdata) 
        if not d.status_code == 200: 
            pytest.fail('There was a problem performing cleanup') 

        check_response = api.get(self.session,profile_url) 
        assert check_response.json()['show_pic'] == 0
"""
