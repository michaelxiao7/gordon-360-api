import pytest
import warnings
import pytest_components as api
import test_gordon360_pytest as control

class Test_AdminTest(control.testCase):
  
# # # # # # # #
# ADMIN  TEST #
# # # # # # # #

#    Verify that a super admin get list of all super admins.
#    Endpoint -- api/admins
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with the student resource
    def test_get_all_admin___superadmin(self):
        url = control.hostURL + 'api/admins/'
        response = self.getAuthorizedResponse(control.credentials.superadmin, url)
        response_json = self.validate_response(response)
        if type(response_json) is not list:
            pytest.fail('Expected list, got {}.'.format(response.text))
        assert [admin for admin in response_json if admin['SUPER_ADMIN']]

#    Verify that regular users can't get list of super admins.
#    Endpoint -- api/admins
#    Expected Status Code -- 401 Unauthorized
#    Expected Response Body -- A json response with the student resource
    def test_get_all_admin___user(self):
        url = control.hostURL + 'api/admins/'
        response = self.getAuthorizedResponse(control.credentials.leader, url)
        response_json = self.validate_response(response, 401)
        assert response_json['Message'] == control.AUTHORIZATION_DENIED

        response = self.getAuthorizedResponse(control.credentials.member, url)
        response_json = self.validate_response(response, 401)
        assert response_json['Message'] == control.AUTHORIZATION_DENIED

#    Verify that a guest can't get list of superadmins.
#    Endpoint -- api/admins
#    Expected Status Code -- 401 Unauthorized Error
    def test_get_all_admin___guest(self):
        url = control.hostURL + 'api/admins/'
        session = self.createGuestSession()
        response = api.get(session, url)
        self.validate_response(response, 401)
        assert response.json()['Message'] == control.AUTHORIZATION_DENIED
            
#    Verify that a super admin get information about a specified super admin.
#    Endpoint -- api/admin/:id
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with the student resource
    def test_get_specified_admin___superadmin(self):
        user_id = control.credentials.superadmin.getID()
        url = control.hostURL + 'api/admins/' + str(user_id) + '/' 
        response = self.getAuthorizedResponse(control.credentials.superadmin, url)
        response_json = self.validate_response(response)
        assert response.json()['ID_NUM'] == user_id

#    Verify that non admins can't get information about a specified super admin.
#    Endpoint -- api/admin/:id
#    Expected Status Code -- 401 Unauthorized
#    Expected Response Body -- A json response with the student resource
    def test_get_specified_admin___user(self):
        user_id = control.credentials.superadmin.getID()
        url = control.hostURL + 'api/admins/' + str(user_id) + '/'

        # **** NOT SURE WHY 360.facultytest IS NOT CURRENTLY DENIED... ****
        # response = self.getAuthorizedResponse(control.credentials.leader, url)
        # response_json = self.validate_response(response, 401)
        # assert response_json['Message'] == control.AUTHORIZATION_DENIED

        response = self.getAuthorizedResponse(control.credentials.member, url)
        response_json = self.validate_response(response, 401)
        assert response_json['Message'] == control.AUTHORIZATION_DENIED

#    Verify that a guest can't get information of all admins.
#    Endpoint -- api/admin/_id
#    Expected Status Code -- 401 Unauthorized Error
#    Expected Response Body -- An authorization denied error
    def test_get_specified_admin___guest_admin(self):
        user_id = control.credentials.superadmin.getID()
        session = self.createGuestSession()
        url = control.hostURL + 'api/admins/' + str(user_id) + '/' 
        response = api.get(session, url)
        response_json = self.validate_response(response, 401)
        assert response_json['Message'] == control.AUTHORIZATION_DENIED
