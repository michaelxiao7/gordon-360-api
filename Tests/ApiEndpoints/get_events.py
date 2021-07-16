#!/usr/bin/env python3

import requests
import pytest_components as api

def createGuestSession():
    """Create a guest session to test guest calls."""
    return requests.Session()

def get_events():
    session = createGuestSession()
    url = "https://25live.collegenet.com/25live/data/gordon/run/events.xml?/&event_type_id=14+57&state=2&end_after=20210515&scope=extended"
    response = api.get(session, url)
    if response.status_code != 200:
        print(f"Expected Status 200, got {response.status_code}")
        exit(1)
    else:
        print("Response: OK")

    try:
        print(response.text[:100])
    except ValueError:
        print(f"Invalid response")

if __name__ == "__main__":
    get_events()
