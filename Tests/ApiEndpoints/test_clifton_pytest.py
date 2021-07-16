import pytest
import warnings
import Control
import pytest_components as api
import pytest_credentials as credentials

ROUTE_PREFIX = "api/profiles/clifton"

class Test_AllProfilesCliftonTest(Control.Control):

# # # # # # # # #
# PROFILE CLIFTON STRENGTHS TESTS #
# # # # # # # # #

#    Verify that a student user can get meal plan data.
#    Endpoint -- api/profile/clifton/{username}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- A json response with dict containing the
#    student mealplan data
    def test_get_clifton_strengths(self):
        url = "/".join([Control.hostURL, ROUTE_PREFIX, "cameron.abbot", "/"])
#        url = "/".join([Control.hostURL, ROUTE_PREFIX, "jonathan.senning", "/"])
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        if response_json is not None:
            try:
                strengths = response_json["Strengths"]
                assert len(strengths) == 5
            except TypeError:
                pytest.fail("Didn't get what I was expecting")
#        assert response_json == "0"  # Test student should have $0 balance
