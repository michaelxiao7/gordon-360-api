import pytest
import warnings
#import test_gordon360_pytest as control
import Control
import pytest_components as api
import pytest_credentials as credentials

ROUTE_PREFIX = "/".join([Control.hostURL, "api/accounts"])

class Test_AllAccountTest(Control.Control):
# # # # # # # # #
# ACCOUNT TESTS #
# # # # # # # # #

#    Verify that a group administrator can get account by email
#    Endpoint -- api/accounts/email/{email}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- profile of the email person
    def test_get_user_by_email(self):
        username = credentials.groupadmin.username
        url = "/".join([ROUTE_PREFIX, "email", username + "@gordon.edu","/"])
        response = self.getAuthorizedResponse(credentials.groupadmin, url)
        response_json = self.validate_response(response)
        assert response_json["ADUserName"].lower() == username.lower()
        if "GordonID" in response_json:
            warnings.warn("Security fault, Gordon ID leak")

#    Verify that a group administrator can search by username 
#    Endpoint -- api/accounts/username/{username}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- profile info of {username}
    def test_get_user_by_username(self):
        username = credentials.groupadmin.username
        url = "/".join([ROUTE_PREFIX, "username",  username, "/"])
        response = self.getAuthorizedResponse(credentials.groupadmin, url)
        response_json = self.validate_response(response)
        assert response_json["ADUserName"].lower() == username.lower()
        if "GordonID" in response_json:
            warnings.warn("Security fault, Gordon ID leak")

#    Verify that someone without group admin priv cannot search by username 
#    Endpoint -- api/accounts/username/{username}
#    Expected Status Code -- 401 Unauthorized
#    Expected Response Body -- profile info of {username}
    def test_get_user_by_username___student(self):
        #import Credentials
        #from getpass import getpass
        #A = input("Username: ")
        #B = getpass("Password: ")
        cred = credentials.student #Credentials.Credentials(1, A, B)
        username = credentials.faculty.username
        url = "/".join([ROUTE_PREFIX, "username",  username, "/"])
        response = self.getAuthorizedResponse(cred,url) #(credentials.student, url)
        response_json = self.validate_response(response, 401)
        assert response_json['Message'] == Control.AUTHORIZATION_DENIED
    
#    Verify that a user can search by a single substring of first or last name
#    Endpoint -- api/accounts/search/{searchString}
#    Expected Status Code -- 200 OK
#    Expected Response Body -- any info that has the searchString
    def test_search_by_string(self):
        for searchString in credentials.staff.username.split("."):
            url = "/".join([ROUTE_PREFIX, "search", searchString, "/"])
            response = self.getAuthorizedResponse(credentials.student, url)
            response_json = self.validate_response(response)
            if type(response_json) is not list:
                pytest.fail("Expected list, got {}.".format(response.text))
            if len(response_json) == 0:
                warnings.warn("No users found to match search string")
            # Search string should appear in either first or last name of
            # each entry of returned list
            for user in response_json:
                assert (searchString.lower() in user["FirstName"].lower() 
                    or searchString.lower() in user["LastName"].lower()
                    or searchString.lower() in user["UserName"].lower())

#    Verify that a user can search by substrings of both first and last names
#    Endpoint -- api/accounts/search/:searchString1/:searchString2
#    Expected Status Code -- 200 OK
#    Expected Response Body -- any info that has both searchStrings
    def test_search_by_two_strings(self):
        s1, s2 = Control.VALID_STUDENT.split(".")
        #s1, s2 = Control.VALID_FACULTY.split(".")
        #s1, s2 = credentials.faculty.username.split(".")
        url = "/".join([ROUTE_PREFIX, "search", s1, s2, "/"])
        response = self.getAuthorizedResponse(credentials.student, url)
        response_json = self.validate_response(response)
        if type(response_json) is not list:
            pytest.fail("Expected list, got {}.".format(response.text))
        if len(response_json) == 0:
            warnings.warn("No users found to match search string")
        # Search strings should appear in either first and last names
        # of each entry of returned list
        for user in response_json:
            assert (s1.lower() in user["FirstName"].lower()
                and s2.lower() in user["LastName"].lower())

#    Verify that an authorized user can perform various advanced searches
#    Endpoint -- api/accounts/advanced-people-search/
#                       {includeStudentSearchParam}/
#                       {includeFacStaffSearchParam}/
#                       {includeAlumniSearchParam}/
#                       {firstNameSearchParam}/
#                       {lastNameSearchParam}/
#                       {majorSearchParam}/
#                       {minorSearchParam}/
#                       {hallSearchParam}/
#                       {classTypeSearchParam}/
#                       {hometownSearchParam}/
#                       {stateSearchParam}/
#                       {countrySearchParam}/
#                       {departmentSearchParam}/
#                       {buildingSearchParam}/
#    Expected Status Code -- 200 OK
#    Expected Response Body -- list of dictionaries
    def test_advanced_people_search(self):
        import xml.etree.ElementTree as ET

        # CLASSDICT: Map strings defined in 
        # - gordon-360-ui/src/views/PeopleSearch/index.js
        # - gordon-360-ui/src/views/PeopleSearch/components/PeopleSearchResult/index.js
        # to numeric values returned by API
        CLASSDICT = {
            "Unassigned": 0,
            "First Year": 1,
            "Sophomore": 2,
            "Junior": 3,
            "Senior": 4,
            "Graduate Student": 5,
            "Undergraduate Conferred": 6,
            "Graduate Conferred": 7,
        }

        doc = ET.parse("advanced-search.xml")
        advancedSearch = doc.getroot()

        # The URL sent to the API has twelve fields.  Fields which are blank
        # (unspecifed) are denoted by 'C#' except that the '#' is really the
        # music sharp character u"\u266F".  This function is passed variable
        # that is either a string or None and either the original string or
        # the C-sharp string is returned.
        stringify = lambda s: str(s) if s is not None else "C" + u"\u266F"

        # String data entered by the user is mapped to lowercase by the UI
        # so we need to do that here.  If the input variable is None, however,
        # we don't want to do anything.  This function accepts a varible and
        # returns a lowercase version of it if it is a string otherwise it
        # just returns the variable.
        lowerIfNotNone = lambda s: s.lower() if type(s) == str else s

        # We're potentially going to make many calls to the API so we create
        # a single authorized session for all of them.
        session = self.createAuthorizedSession(credentials.faculty, ROUTE_PREFIX)
        for user in advancedSearch:
            usertype = user.get("type")
            username = lowerIfNotNone(user.findtext("username"))
            firstname = lowerIfNotNone(user.findtext("firstname"))
            lastname = lowerIfNotNone(user.findtext("lastname"))
            major = user.findtext("major")
            minor = user.findtext("minor")
            hall = user.findtext("hall")
            classtype = user.findtext("classtype")
            if classtype is not None:
                classtype = CLASSDICT[classtype]
            hometown = lowerIfNotNone(user.findtext("hometown"))
            state = user.findtext("state")
            country = user.findtext("country")
            department = user.findtext("department")
            building = user.findtext("building")
        
            url = "/".join([
                ROUTE_PREFIX,
                "advanced-people-search",
                str(usertype == "student").lower(), # either "true" or "false"
                str(usertype == "facstaff").lower(),
                str(usertype == "alum").lower(),
                stringify(firstname),
                stringify(lastname),
                stringify(major),
                stringify(minor),
                stringify(hall),
                stringify(classtype),
                stringify(hometown),
                stringify(state),
                stringify(country),
                stringify(department),
                stringify(building),
                "/"])

            response = api.get(session, url)
            response_json = self.validate_response(response)
            if type(response_json) is not list:
                pytest.fail("Expected list, got {}.".format(response.text))
            if len(response_json) == 0:
                warnings.warn("No users found: API route: " + url)
                
            # Verify we found valid data
            for foundUser in response_json:
                if firstname is not None:
                    assert firstname in foundUser["FirstName"].lower()
                if lastname is not None:
                    assert lastname in foundUser["LastName"].lower()
                if major is not None:
                    assert major in foundUser["Major1Description"] \
                        or major in foundUser["Major2Description"] \
                        or major in foundUser["Major3Description"]
                if minor is not None:
                    assert minor in foundUser["Minor1Description"] \
                        or minor in foundUser["Minor2Description"] \
                        or minor in foundUser["Minor3Description"]
                if hall is not None:
                    assert hall == foundUser["Hall"]
                if classtype is not None:
                    assert str(classtype) == foundUser["Class"]
                if hometown is not None:
                    assert hometown == foundUser["HomeCity"].lower()
                if state is not None:
                    assert state == foundUser["HomeState"]
                if country is not None:
                    assert country == foundUser["Country"]
                if department is not None:
                    assert department == foundUser["OnCampusDepartment"]
                if building is not None:
                    assert building == foundUser["BuildingDescription"]


    # def test_advanced_people_search(self):
    #     xml = ET.parse("advanced-search.xml")
    #     advancedPeopleSearch = xml.getroot()
    #     for user in xml.getroot():
    #     print(user.get("type"))
    #     for field in FIELDS:
    #         value = user.findtext(field)
    #         if value is not None:
    #             print(f"  {field}: {value}")
    #      session = self.createAuthorizedSession(credentials.student, ROUTE_PREFIX)
    #     # Fac/Staff
    #     firstName, lastName = Control.VALID_FACULTY.lower().split(".")

    """
[
    {
        "Mail_Location": "17",
        "Hall": "Nyland Hall",
        "FirstName": "Cameron",
        "LastName": "Abbot",
        "NickName": "Cameron",
        "Class": "3",
        "Major1Description": "Computer Science",
        "Major2Description": "Economics",
        "Major3Description": "",
        "Minor1Description": "",
        "Minor2Description": "",
        "Minor3Description": "",
        "HomeCity": "Windsor",
        "HomeState": "CT",
        "Country": "",
        "KeepPrivate": "",
        "Email": "Cameron.Abbot@gordon.edu",
        "AD_Username": "Cameron.Abbot",
        "Type": "Student",
        "BuildingDescription": null,
        "OnCampusDepartment": null
    }
]

[
    {
        "Title": null,
        "FirstName": "Jonathan",
        "MiddleName": null,
        "LastName": "Senning",
        "Suffix": null,
        "MaidenName": null,
        "NickName": "Jonathan",
        "OnCampusDepartment": "Mathematics and Computer Science",
        "OnCampusBuilding": null,
        "OnCampusRoom": null,
        "OnCampusPhone": null,
        "OnCampusPrivatePhone": null,
        "OnCampusFax": null,
        "HomePhone": null,
        "HomeCity": "South Hamilton",
        "HomeState": "MA",
        "HomeCountry": null,
        "KeepPrivate": "0",
        "JobTitle": "Professor of Mathematics & Computer Science",
        "SpouseName": null,
        "Dept": null,
        "Gender": null,
        "Email": "Jonathan.Senning@gordon.edu",
        "Type": "Faculty",
        "AD_Username": "Jonathan.Senning",
        "office_hours": null,
        "preferred_photo": null,
        "show_pic": null,
        "BuildingDescription": "Ken Olsen Science Center",
        "Country": null,
        "Mail_Location": "",
        "Hall": null,
        "Class": null,
        "Major1Description": null,
        "Major2Description": null,
        "Major3Description": null,
        "Minor1Description": null,
        "Minor2Description": null,
        "Minor3Description": null
    }
]
    """