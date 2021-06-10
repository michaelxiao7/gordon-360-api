import pytest
import warnings
#import string
#from pytest_components import requests
#from datetime import datetime

#import pytest_components as api
#import test_gordon360_pytest as control

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
        json = response.json()
    except ValueError:
        pytest.fail('Expected JSON response body, got {}.'.format(json))
        # or could format response.text

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
            pytest.fail("Expecting type {} but got type {}".format(type(activity[k]), activityTypes[k]))
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