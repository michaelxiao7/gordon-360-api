﻿using Gordon360.Models;
using Gordon360.Repositories;
using Gordon360.Services;
using Gordon360.Static.Names;
using Gordon360.Static.Methods;
using System;
using System.Linq;
using System.Net.Http;
using System.Security.Claims;
using System.Web.Http.Controllers;
using System.Web.Http.Filters;

namespace Gordon360.AuthorizationFilters
{
    /* Authorization Filter.
     * It is actually an action filter masquerading as an authorization filter. This is because I need access to the 
     * parameters passed to the controller. Authorization Filters don't have that access. Action Filters do.
     * 
     * Because of the nature of how we authorize people, this code might seem very odd, so I'll try to explain. 
     * Proceed at your own risk. If you can understand this code, you can understand the whole project. 
     * 
     * 1st Observation: You can't authorize access to a resource that isn't owned by someone. Resources like Sessions, Participations,
     * and Activity Definitions are accessibile by anyone.
     * 2nd Observation: To Authorize someone to perform an action on a resource, you need to know the following:
     * 1. Who is to be authorized? 2.What resource are they trying to access? 3. What operation are they trying to make on the resource?
     * This "algorithm" uses those three points and decides through a series of switch statements if the current user
     * is authorized.
     */
    public class StateYourBusiness : ActionFilterAttribute
    {
        // Resource to be accessed: Will get as parameters to the attribute
        public string resource { get; set; }
        // Operation to be performed: Will get as parameters to the attribute
        public string operation { get; set; }

        private HttpActionContext context;

        // User position at the college and their id.
        private string user_position { get; set; }
        private string user_id { get; set; }
        private string user_name { get; set; }

        private bool isAuthorized = false;

        public override void OnActionExecuting(HttpActionContext actionContext)
        {
            context = actionContext;
            // Step 1: Who is to be authorized
            var authenticatedUser = actionContext.RequestContext.Principal as ClaimsPrincipal;

            if (authenticatedUser.Claims.FirstOrDefault(x => x.Type == "college_role") != null)
            {
                user_position = authenticatedUser.Claims.FirstOrDefault(x => x.Type == "college_role").Value;
                user_id = authenticatedUser.Claims.FirstOrDefault(x => x.Type == "id").Value;
                user_name = authenticatedUser.Claims.FirstOrDefault(x => x.Type == "user_name").Value;

                // Keeping these for now commented out as more permissions testing needs to be done in future
                //System.Diagnostics.Debug.WriteLine("User name: " + user_name);
                //System.Diagnostics.Debug.WriteLine("User Position: " + user_position);

                if (user_position == Position.SUPERADMIN)
                {
                    var adminService = new AdministratorService(new UnitOfWork());
                    var admin = adminService.Get(user_id);

                    // If user is super admin, skip verification steps and return.
                    if (admin.SUPER_ADMIN)
                    {
                        base.OnActionExecuting(actionContext);
                        return;
                    }
                }
            }
           
            // Can the user perform the operation on the resource?
            isAuthorized = canPerformOperation(resource, operation);
            if (!isAuthorized)
            {
                actionContext.Response = actionContext.Request.CreateResponse(System.Net.HttpStatusCode.Unauthorized,  new { Message = "Authorization has been denied for this request." });
            }

            base.OnActionExecuting(actionContext);
        }

       
        private bool canPerformOperation(string resource, string operation)
        {
            switch(operation)
            {
                case Operation.READ_ONE: return canReadOne(resource);
                case Operation.READ_ALL: return canReadAll(resource);
                case Operation.READ_PARTIAL: return canReadPartial(resource);
                case Operation.ADD: return canAdd(resource);
                case Operation.DENY_ALLOW: return canDenyAllow(resource);
                case Operation.UPDATE: return canUpdate(resource);
                case Operation.DELETE: return canDelete(resource);
                case Operation.READ_PUBLIC: return canReadPublic(resource);
                default: return false;
            }
        }

        /*
         * Operations
         */
         // This operation is specifically for authorizing deny and allow operations on membership requests. These two operations don't
         // Fit in nicely with the REST specification which is why there is a seperate case for them.
         private bool canDenyAllow(string resource)
        {
            // User is admin
            if (user_position == Position.SUPERADMIN)
                return true;

            switch (resource)
            {
                
                case Resource.MEMBERSHIP_REQUEST:
                    {
                        var mrID = (int)context.ActionArguments["id"];
                        // Get the view model from the repository
                        var mrService = new MembershipRequestService(new UnitOfWork());
                        var mrToConsider = mrService.Get(mrID);
                        // Populate the membershipRequest manually. Omit fields I don't need.
                        var activityCode = mrToConsider.ActivityCode;
                        var membershipService = new MembershipService(new UnitOfWork());
                        var is_activityLeader = membershipService.GetLeaderMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (is_activityLeader) // If user is the leader of the activity that the request is sent to.
                            return true;
                        var is_activityAdvisor = membershipService.GetAdvisorMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (is_activityAdvisor) // If user is the advisor of the activity that the request is sent to.
                            return true;

                        return false;
                    }
                default: return false;
                    
            }
        }

         private bool canReadOne(string resource)
        {
            // User is admin
            if (user_position == Position.SUPERADMIN)
                return true;

            switch (resource)
            {
                case Resource.PROFILE:
                    return true;
                case Resource.EMERGENCY_CONTACT:
                    if (user_position == Position.POLICE)
                        return true;
                    else
                    {
                        var username = (string)context.ActionArguments["username"];
                        var isSelf = username.Equals(user_name.ToLower());
                        return isSelf;
                    }
                case Resource.MEMBERSHIP:
                    return true;
                case Resource.MEMBERSHIP_REQUEST:
                    {
                        // membershipRequest = mr
                        var mrService = new MembershipRequestService(new UnitOfWork());
                        var mrID = (int)context.ActionArguments["id"];
                        var mrToConsider = mrService.Get(mrID);
                        var is_mrOwner = mrToConsider.IDNumber.ToString() == user_id; // User_id is an instance variable.

                        if (is_mrOwner) // If user owns the request
                            return true;

                        var activityCode = mrToConsider.ActivityCode;
                        var membershipService = new MembershipService(new UnitOfWork());
                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin) // If user is a group admin of the activity that the request is sent to
                            return true;

                        return false;
                    }
                case Resource.STUDENT:
                    // To add a membership for a student, you need to have the students identifier.
                    // NOTE: I don't believe the 'student' resource is currently being used in API
                    {
                        return true;
                    }
                case Resource.ADVISOR:
                    return true;
                case Resource.ACCOUNT:
                    {
                        // Membership group admins can access ID of members using their email
                        // NOTE: In the future, probably only email addresses should be stored 
                        // in memberships, since we would rather not give students access to
                        // other students' account information
                        var membershipService = new MembershipService(new UnitOfWork());
                        var isGroupAdmin = membershipService.IsGroupAdmin(Int32.Parse(user_id));
                        if (isGroupAdmin) // If user is a group admin of the activity that the request is sent to
                            return true;

                        // faculty and police can access student account information
                        if (user_position == Position.FACSTAFF
                            || user_position == Position.POLICE)
                            return true;

                        return false;
                    }
                case Resource.HOUSING:
                    {
                        // The members of the apartment application can only read their application
                        HousingService housingService = new HousingService(new UnitOfWork());
                        string sess_cde = Helpers.GetCurrentSession().SessionCode;
                        int? applicationID = housingService.GetApplicationID(user_name, sess_cde);
                        int requestedApplicationID = (int)context.ActionArguments["applicationID"];
                        if (applicationID.HasValue && applicationID.Value == requestedApplicationID)
                        {
                            return true;
                        }
                        return false;
                    }
                case Resource.NEWS:
                    return true;
                default: return false;
                    
            }
        }
        // For reads that access a group of resources filterd in a specific way 
        private bool canReadPartial(string resource)
        {
            // User is admin
            if (user_position == Position.SUPERADMIN)
                return true;

            switch (resource)
            {
                case Resource.MEMBERSHIP_BY_ACTIVITY:
                    {
                        // Only people that are part of the activity should be able to see members
                        var membershipService = new MembershipService(new UnitOfWork());
                        var activityCode = (string)context.ActionArguments["id"];
                        var activityMembers = membershipService.GetMembershipsForActivity(activityCode);
                        var is_personAMember = activityMembers.Where(x => x.IDNumber.ToString() == user_id && x.Participation != "GUEST").Count() > 0;
                        if (is_personAMember)
                            return true;
                        return false;
                    }
                case Resource.MEMBERSHIP_BY_STUDENT:
                    {
                        // Only the person itself or an admin can see someone's memberships
                        return (string)context.ActionArguments["id"] == user_id;
                    }

                case Resource.EVENTS_BY_STUDENT_ID:
                    {
                        // Only the person itself or an admin can see someone's chapel attendance
                        var username_requested = context.ActionArguments["username"];
                        var is_creditOwner = username_requested.ToString().Equals(user_name);
                        return is_creditOwner;
                    }


                case Resource.MEMBERSHIP_REQUEST_BY_ACTIVITY:
                    {
                        // An activity leader should be able to see the membership requests that belong to the activity he is leading.
                        var membershipService = new MembershipService(new UnitOfWork());
                        var activityCode = (string)context.ActionArguments["id"];
                        var groupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode);
                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin) // If user is a group admin of the activity that the request is sent to
                            return true;
                        return false;
                    }
                // Since the API only allows asking for your requests (no ID argument), it's always OK.
                case Resource.MEMBERSHIP_REQUEST_BY_STUDENT:
                    {
                        return true;
                    }
                 // Only activity leaders/advisors should be to get emails for his/her members.
                case Resource.EMAILS_BY_ACTIVITY:
                    {
                        var activityCode = (string)context.ActionArguments["id"];
                        var membershipService = new MembershipService(new UnitOfWork());
                        var leaders = membershipService.GetLeaderMembershipsForActivity(activityCode);
                        var is_activity_leader = leaders.Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (is_activity_leader)
                            return true;

                        var advisors = membershipService.GetAdvisorMembershipsForActivity(activityCode);
                        var is_activityAdvisor = advisors.Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (is_activityAdvisor)
                            return true;

                        var groupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode);
                        var is_groupAdmin = groupAdmin.Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (is_groupAdmin)
                            return true;
                        return false;
                    }
                // Anyone who is already logged in can contact the leaders or group admin ("primary contact")
                case Resource.EMAILS_BY_LEADERS:
                    {
                        return true;
                    }
                case Resource.EMAILS_BY_GROUP_ADMIN:
                    {
                        return true;
                    }
                case Resource.ADVISOR_BY_ACTIVITY:
                    {
                        return true;
                    }
                case Resource.LEADER_BY_ACTIVITY:
                    {
                        return true;
                    }
                case Resource.GROUP_ADMIN_BY_ACTIVITY:
                    {
                        return true;
                    }
                case Resource.NEWS:
                    {
                        return true;
                    }
                default: return false;
            }
        }
        private bool canReadAll(string resource)
        {
            switch (resource)
            {
                case Resource.MEMBERSHIP:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false;
                case Resource.ChapelEvent:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false;
                case Resource.EVENTS_BY_STUDENT_ID:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false;

                case Resource.MEMBERSHIP_REQUEST:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false;
                case Resource.STUDENT:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false; // See reasons for this in CanReadOne(). No one (except for super admin) should be able to access student records through
                        // our API.
                case Resource.ADVISOR:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false;
                case Resource.GROUP_ADMIN:
                    // User is site-wide admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false;
                case Resource.ACCOUNT:
                    return false;
                case Resource.ADMIN:
                    return false;
                case Resource.HOUSING:
                    {
                        // Only the housing admin and super admin can read all of the received applications.
                        // Super admin has unrestricted access by default, so no need to check.
                        var housingService = new HousingService(new UnitOfWork());
                        if (housingService.CheckIfHousingAdmin(user_id))
                        {
                            return true;
                        }
                        return false;
                    }
                case Resource.NEWS:
                    return true;
                default: return false;
            }
        }

        private bool canReadPublic(string resource)
        {
            switch (resource)
            {
                case Resource.SLIDER:
                    return true;
                case Resource.NEWS:
                    return false;
                default: return false;

            }
        }
        private bool canAdd(string resource)
        {
            switch (resource)
            {
                case Resource.SHIFT:
                    {
                        if (user_position == Position.STUDENT)
                            return true;
                        return false;
                    }

                case Resource.MEMBERSHIP:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var membershipToConsider = (MEMBERSHIP)context.ActionArguments["membership"];
                        // A membership can always be added if it is of type "GUEST"
                        var isFollower = (membershipToConsider.PART_CDE == Activity_Roles.GUEST) && (user_id == membershipToConsider.ID_NUM.ToString());
                        if (isFollower)
                            return true;

                        var activityCode = membershipToConsider.ACT_CDE;
                        var membershipService = new MembershipService(new UnitOfWork());

                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin) // If user is the advisor of the activity that the request is sent to.
                            return true;
                        return false;
                    }
                    
                case Resource.MEMBERSHIP_REQUEST:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var membershipRequestToConsider = (REQUEST)context.ActionArguments["membershipRequest"];
                        // A membership request belonging to the currently logged in student
                        var is_Owner = (membershipRequestToConsider.ID_NUM.ToString() == user_id);
                        if (is_Owner)
                            return true;
                        // No one should be able to add requests on behalf of another person.
                        return false;
                    } 
                case Resource.STUDENT:
                    return false; // No one should be able to add students through this API
                case Resource.ADVISOR:
                    // User is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    else
                        return false; // Only super admin can add Advisors through this API
                case Resource.HOUSING_ADMIN:
                    //only superadmins can add a HOUSING_ADMIN
                    return false;
                case Resource.HOUSING:
                    {
                        // The user must be a student and not a member of an existing application
                        var housingService = new HousingService(new UnitOfWork());
                        if (user_position == Position.STUDENT)
                        {
                            var sess_cde = Helpers.GetCurrentSession().SessionCode;
                            int? applicationID = housingService.GetApplicationID(user_name, sess_cde);
                            if (!applicationID.HasValue)
                            {
                                return true;
                            }
                            return false;
                        }
                        return false;
                    }
                case Resource.ADMIN:
                    return false;
                case Resource.ERROR_LOG:
                    return true;
                case Resource.NEWS:
                    return true;  
                default: return false;
            }
        }
        private bool canUpdate(string resource)
        {
            switch (resource)
            {
                case Resource.SHIFT:
                    {
                        if (user_position == Position.STUDENT)
                            return true;
                        return false;
                    }
                case Resource.MEMBERSHIP:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var membershipToConsider = (MEMBERSHIP)context.ActionArguments["membership"];
                        var activityCode = membershipToConsider.ACT_CDE;
                       

                        var membershipService = new MembershipService(new UnitOfWork());
                        //var is_membershipLeader = membershipService.GetLeaderMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        //if (is_membershipLeader)
                        //    return true; // Activity Leaders can update memberships of people in their activity.

                        //var is_membershipAdvisor = membershipService.GetAdvisorMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        //if (is_membershipAdvisor)
                        //    return true; // Activity Advisors can update memberships of people in their activity.
                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin)
                            return true; // Activity Advisors can update memberships of people in their activity.

                        var is_membershipOwner = membershipToConsider.ID_NUM.ToString() == user_id;
                        if (is_membershipOwner)
                        {
                            // Restrict what a regular owner can edit.
                            var originalMembership = membershipService.GetSpecificMembership(membershipToConsider.MEMBERSHIP_ID);
                            // If they are not trying to change their participation level, then it is ok
                            if (originalMembership.PART_CDE == membershipToConsider.PART_CDE)
                                return true;
                        }
                       

                        return false;
                    }
                    
                case Resource.MEMBERSHIP_REQUEST:
                    {
                        // Once a request is sent, no one should be able to edit its contents.
                        // If a mistake is made in creating the original request, the user can always delete it and make a new one.
                        return false;
                    }
                case Resource.MEMBERSHIP_PRIVACY:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var membershipService = new MembershipService(new UnitOfWork());
                        var membershipID = (int)context.ActionArguments["id"];

                        var membershipToConsider = membershipService.GetSpecificMembership(membershipID);
                        var is_membershipOwner = membershipToConsider.ID_NUM.ToString() == user_id;
                        if (is_membershipOwner)
                            return true;

                        var activityCode = membershipToConsider.ACT_CDE;

                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin)
                            return true;

                        return false;
                    }
                case Resource.STUDENT:
                    return false; // No one should be able to update a student through this API
                case Resource.HOUSING:
                    {
                        // The housing admins can update the application information (i.e. probation, offcampus program, etc.)
                        // If the user is a student, then the user must be on an application and be an editor to update the application
                        HousingService housingService = new HousingService(new UnitOfWork());
                        if (housingService.CheckIfHousingAdmin(user_id))
                        {
                            return true;
                        }
                        else if (user_position == Position.STUDENT)
                        {
                            string sess_cde = Helpers.GetCurrentSession().SessionCode;
                            int? applicationID = housingService.GetApplicationID(user_name, sess_cde);
                            int requestedApplicationID = (int)context.ActionArguments["applicationID"];
                            if (applicationID.HasValue && applicationID == requestedApplicationID)
                            {
                                string editorUsername = housingService.GetEditorUsername(applicationID.Value);
                                if (editorUsername.ToLower() == user_name.ToLower())
                                    return true;
                                return false;
                            }
                            return false;
                        }
                        return false;
                    }
                case Resource.ADVISOR:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;

                        var membershipService = new MembershipService(new UnitOfWork());
                        var membershipToConsider = (MEMBERSHIP)context.ActionArguments["membership"];
                        var activityCode = membershipToConsider.ACT_CDE;

                        var is_advisor = membershipService.GetAdvisorMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (is_advisor)
                            return true; // Activity Advisors can update memberships of people in their activity.

                        return false;
                    }
                case Resource.PROFILE:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;

                        var username = (string)context.ActionArguments["username"];
                        var isSelf = username.Equals(user_name);
                        return isSelf;
                    }

                case Resource.ACTIVITY_INFO:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var activityCode = (string)context.ActionArguments["id"];
                        var membershipService = new MembershipService(new UnitOfWork());

                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin)
                            return true;
                        return false;

                    }

                case Resource.ACTIVITY_STATUS:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var activityCode = (string)context.ActionArguments["id"];
                        var sessionCode = (string)context.ActionArguments["sess_cde"];
                        var unitOfWork = new UnitOfWork();

                        var membershipService = new MembershipService(unitOfWork);
                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin)
                        {
                            var activityService = new ActivityService(unitOfWork);
                            // If an activity is currently open, then a group admin has the ability to close it
                            if (activityService.IsOpen(activityCode, sessionCode))
                            {
                                return true;
                            }
                        }   

                        // If an activity is currently closed, only super admin has permission to edit its closed/open status   

                        return false;
                    }
                case Resource.EMERGENCY_CONTACT:
                    {
                        var username = (string)context.ActionArguments["username"];
                        var isSelf = username.Equals(user_name);
                        return isSelf;
                    }

                case Resource.NEWS:
                    var newsID = context.ActionArguments["newsID"];
                    var newsService = new NewsService(new UnitOfWork());
                    var newsItem = newsService.Get((int)newsID);
                    // only unapproved posts may be updated
                    var approved = newsItem.Accepted;
                    if (approved == null || approved == true)
                        return false;
                    // can update if user is admin
                    if (user_position == Position.SUPERADMIN)
                        return true;
                    // can update if user is news item author
                    string newsAuthor = newsItem.ADUN;
                    if (user_name == newsAuthor)
                        return true;
                    return false;
                default: return false;
            }
        }
        private bool canDelete(string resource)
        {
            switch (resource)
            {
                case Resource.SHIFT:
                    if (user_position == Position.STUDENT)
                        return true;
                    return false;
                case Resource.MEMBERSHIP:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        var membershipService = new MembershipService(new UnitOfWork());
                        var membershipID = (int)context.ActionArguments["id"];
                        var membershipToConsider = membershipService.GetSpecificMembership(membershipID);
                        var is_membershipOwner = membershipToConsider.ID_NUM.ToString() == user_id;
                        if (is_membershipOwner)
                            return true;

                        var activityCode = membershipToConsider.ACT_CDE;

                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin)
                            return true;
                        
                        return false;
                    }
                case Resource.MEMBERSHIP_REQUEST:
                    {
                        // User is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        // membershipRequest = mr
                        var mrService = new MembershipRequestService(new UnitOfWork());
                        var mrID = (int)context.ActionArguments["id"];
                        var mrToConsider = mrService.Get(mrID);
                        var is_mrOwner = mrToConsider.IDNumber.ToString() == user_id;
                        if (is_mrOwner)
                            return true;

                        var activityCode = mrToConsider.ActivityCode;
                        var membershipService = new MembershipService(new UnitOfWork());

                        var isGroupAdmin = membershipService.GetGroupAdminMembershipsForActivity(activityCode).Where(x => x.IDNumber.ToString() == user_id).Count() > 0;
                        if (isGroupAdmin)
                            return true;


                        return false;
                    }
                case Resource.STUDENT:
                    return false; // No one should be able to delete a student through our API
                case Resource.HOUSING:
                    {
                        // The housing admins can update the application information (i.e. probation, offcampus program, etc.)
                        // If the user is a student, then the user must be on an application and be an editor to update the application
                        HousingService housingService = new HousingService(new UnitOfWork());
                        if (housingService.CheckIfHousingAdmin(user_id))
                        {
                            return true;
                        }
                        else if (user_position == Position.STUDENT)
                        {
                            string sess_cde = Helpers.GetCurrentSession().SessionCode;
                            int? applicationID = housingService.GetApplicationID(user_name, sess_cde);
                            int requestedApplicationID = (int)context.ActionArguments["applicationID"];
                            if (applicationID.HasValue && applicationID.Value == requestedApplicationID)
                            {
                                var editorUsername = housingService.GetEditorUsername(applicationID.Value);
                                if (editorUsername.ToLower() == user_name.ToLower())
                                    return true;
                                return false;
                            }
                            return false;
                        }
                        return false;
                    }
                case Resource.ADVISOR:
                    return false;
                case Resource.ADMIN:
                    return false;
                case Resource.HOUSING_ADMIN:
                    {
                        // Only the superadmins can remove a housing admin from the whitelist
                        // Super admins have unrestricted access by default: no need to check
                        return false;
                    }
                case Resource.NEWS:
                    {
                        var newsID = context.ActionArguments["newsID"];
                        var newsService = new NewsService(new UnitOfWork());
                        var newsItem = newsService.Get((int)newsID);
                        // only expired news items may be deleted
                        var todaysDate = System.DateTime.Now;
                        var newsDate = (System.DateTime)newsItem.Entered;
                        var dateDiff = (todaysDate - newsDate).Days;
                        if (newsDate == null || dateDiff >= 14)
                        {
                            return false;
                        }
                        // user is admin
                        if (user_position == Position.SUPERADMIN)
                            return true;
                        // user is news item author
                        string newsAuthor = newsItem.ADUN;
                        if (user_name == newsAuthor)
                            return true;
                        return false;
                    }
                default: return false;
            }
        }

       
    }
}
