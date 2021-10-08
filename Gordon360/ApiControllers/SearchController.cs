using System;
using System.Security.Claims;
using System.Linq;
using Gordon360.Static.Data;
using Gordon360.Static.Names;
using Gordon360.Static.Methods;
using System.Web.Http;
using Gordon360.Exceptions.ExceptionFilters;
using Gordon360.Repositories;
using Gordon360.Services;
using Gordon360.Exceptions.CustomExceptions;
using System.Collections.Generic;
using Gordon360.Models.ViewModels;
using System.Text.RegularExpressions;
using Newtonsoft.Json.Linq;
using Gordon360.AuthorizationFilters;

namespace Gordon360.ApiControllers
{
    [Authorize]
    [CustomExceptionFilter]
    [RoutePrefix("api/search")]
    public class SearchController : ApiController
    {
        private IRoleCheckingService _roleCheckingService;

        IAccountService _accountService;
        IEventService _eventService;
        IActivityService _activityService;

        public SearchController()
        {
            IUnitOfWork _unitOfWork = new UnitOfWork();
            _accountService = new AccountService(_unitOfWork);
            _eventService = new EventService(_unitOfWork);
            _activityService = new ActivityService(_unitOfWork);
            _roleCheckingService = new RoleCheckingService(_unitOfWork);
        }

        /// <summary>
        /// Return a list of accounts matching some or all of the search parameter
        /// </summary>
        /// 
        /// 
        /// Full Explanation:
        /// 
        /// Returns a list of accounts ordered by key of a combination of users first/last/user name in the following order
        ///     1.first or last name begins with search query,
        ///     2.first or last name in Username that begins with search query
        ///     3.first or last name that contains the search query
        ///     
        /// If Full Names of any two accounts are the same the follow happens to the dictionary key to solve this problem
        ///     1. If there is a number attached to their account this is appened to the end of their key
        ///     2. Otherwise an '1' is appended to the end
        ///     
        /// Note:
        /// A '1' is added inbetween a key's first and last name or first and last username in order to preserve the presedence set by shorter names
        /// as both first and last are used as a part of the key in order to order matching first/last names with the remaining part of their name
        /// but this resulted in the presedence set by shorter names to be lost
        /// 
        /// Note:
        /// "z" s are added in order to keep each case split into each own group in the dictionary
        /// 
        /// <param name="searchString"> The input to search for </param>
        /// <returns> All accounts meeting some or all of the parameter</returns>
        [HttpGet]
        [Route("search/{searchString}")]
        public IHttpActionResult Search(string searchString)
        {
            var accounts = SearchAccounts(searchString);
            var activities = SearchActivities(searchString);
            var all = accounts.Concat(activities).OrderBy((s) => s.Precedence);
            return Ok(all);

            //var events = Data.AllEvents;
        }

        public IEnumerable<SearchResultViewModel> SearchAccounts(string searchString)
        {
            //get token data from context, username is the username of current logged in person
            var authenticatedUser = ActionContext.RequestContext.Principal as ClaimsPrincipal;
            var viewerName = authenticatedUser.Claims.FirstOrDefault(x => x.Type == "user_name").Value;
            var viewerType = _roleCheckingService.getCollegeRole(viewerName);

            var accounts = Data.AllBasicInfoWithoutAlumni;

            int precedence = 0;

            var allMatches = new SortedDictionary<string, SearchResultViewModel>();
            IEnumerable<SearchResultViewModel> ret;

            Action<string, SearchResultViewModel> appendMatch = (string key, SearchResultViewModel match) =>
            {
                while (allMatches.ContainsKey(key))
                {
                    key += "1";
                };
                allMatches.Add(key, match);
            };


            if (!string.IsNullOrEmpty(searchString))
            {

                // First name exact match (Highest priority)
                foreach (var match in accounts.Where(s => s.FirstNameMatches(searchString)))
                {
                    string key = GenerateKey(match.FirstName, match.LastName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Nickname exact match
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.NicknameMatches(searchString)))
                {
                    string key = GenerateKey(match.FirstName, match.LastName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Last name exact match
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.LastNameMatches(searchString)))
                {
                    string key = GenerateKey(match.LastName, match.FirstName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Maiden name exact match
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.MaidenNameMatches(searchString)))
                {
                    string key = GenerateKey(match.LastName, match.FirstName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // First name starts with
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.FirstNameStartsWith(searchString)))
                {
                    string key = GenerateKey(match.FirstName, match.LastName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Username (first name) starts with
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.UsernameFirstNameStartsWith(searchString)))
                {
                    string key = GenerateKey(match.GetFirstNameFromUsername(), match.GetLastNameFromUsername(), match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Nickname starts with
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.NicknameStartsWith(searchString)))
                {
                    string key = GenerateKey(match.FirstName, match.LastName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Last name starts with
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.LastNameStartsWith(searchString)))
                {
                    string key = GenerateKey(match.LastName, match.FirstName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Maiden name starts with
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.MaidenNameStartsWith(searchString)))
                {
                    string key = GenerateKey(match.LastName, match.FirstName, match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Username (last name) starts with
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.UsernameLastNameStartsWith(searchString)))
                {
                    string key = GenerateKey(match.GetLastNameFromUsername(), match.GetFirstNameFromUsername(), match.UserName, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // First name, last name, nickname, maidenname or username contains (Lowest priority)
                foreach (var match in accounts
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.FirstNameContains(searchString) || s.NicknameContains(searchString) || s.LastNameContains(searchString) || s.MaidenNameContains(searchString) || s.UsernameContains(searchString)))
                {
                    string key;
                    if (match.FirstNameContains(searchString))
                    {
                        key = GenerateKey(match.FirstName, match.LastName, match.UserName, precedence);
                    }
                    else if (match.NicknameContains(searchString))
                    {
                        key = GenerateKey(match.FirstName, match.LastName, match.UserName, precedence);
                    }
                    else if (match.LastNameContains(searchString))
                    {
                        key = GenerateKey(match.LastName, match.FirstName, match.UserName, precedence);
                    }
                    else if (match.MaidenNameContains(searchString))
                    {
                        key = GenerateKey(match.LastName, match.FirstName, match.UserName, precedence);
                    }
                    else
                    {
                        key = GenerateKey(match.UserName, "", match.UserName, precedence);
                    }

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }

                allMatches.OrderBy(m => m.Key);
                ret = allMatches.Values;
            }
            else {
                ret = accounts.Select((x) => (SearchResultViewModel)x);
            }

            // Return all of the 
            return ret;
        }



        public IEnumerable<SearchResultViewModel> SearchActivities(string searchString)
        {
            //get token data from context, username is the username of current logged in person
            var authenticatedUser = ActionContext.RequestContext.Principal as ClaimsPrincipal;
            var viewerName = authenticatedUser.Claims.FirstOrDefault(x => x.Type == "user_name").Value;
            var viewerType = _roleCheckingService.getCollegeRole(viewerName);
            
            var activities = _activityService.GetActivitiesForSession(Helpers.GetCurrentSession().SessionCode);

            int precedence = 0;

            var allMatches = new SortedDictionary<string, SearchResultViewModel>();
            IEnumerable<SearchResultViewModel> ret;

            Action<string, SearchResultViewModel> appendMatch = (string key, SearchResultViewModel match) =>
            {
                while (allMatches.ContainsKey(key))
                {
                    key += "1";
                };
                allMatches.Add(key, match);
            };


            if (!string.IsNullOrEmpty(searchString))
            {

                // Code name exact match (Highest priority)
                foreach (var match in activities.Where(s => s.ActivityCodeMatches(searchString)))
                {
                    string key = GenerateKey(match.ActivityCode, match.ActivityDescription, match.ActivityType, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Desc exact match
                foreach (var match in activities
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.ActivityDescriptionMatches(searchString)))
                {
                    string key = GenerateKey(match.ActivityCode, match.ActivityDescription, match.ActivityType, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Type exact match
                foreach (var match in activities
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.ActivityTypeMatches(searchString)))
                {
                    string key = GenerateKey(match.ActivityCode, match.ActivityDescription, match.ActivityType, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, searchmatch);
                }
                precedence++;

                // Desc starts with
                foreach (var match in activities
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.ActivityDescriptionStartsWith(searchString)))
                {
                    string key = GenerateKey(match.ActivityCode, match.ActivityDescription, match.ActivityType, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, (SearchResultViewModel)match);
                }
                precedence++;

                // Desc contains
                foreach (var match in activities
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.ActivityDescriptionContains(searchString)))
                {
                    string key = GenerateKey(match.ActivityCode, match.ActivityDescription, match.ActivityType, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, (SearchResultViewModel)match);
                }
                precedence++;

                // Blurb contains
                foreach (var match in activities
                                        .Where(s => !allMatches.ContainsValue(s))
                                        .Where(s => s.ActivityBlurbContains(searchString)))
                {
                    string key = GenerateKey(match.ActivityCode, match.ActivityDescription, match.ActivityType, precedence);

                    var searchmatch = (SearchResultViewModel)match;
                    searchmatch.Precedence = precedence;

                    appendMatch(key, match);
                }
                precedence++;

                allMatches.OrderBy(m => m.Key);
                ret = allMatches.Values;
            }
            else
            {
                ret = activities.Select((x) => (SearchResultViewModel)x);
            }

            // Return all of the 
            return ret;
        }

        /// <Summary>
        ///   This function generates a key for each account
        /// </Summary>
        ///
        /// <param name="keyPart1">This is what you would want to sort by first, used for first part of key</param>
        /// <param name="keyPart2">This is what you want to sort by second, used for second part of key</param>
        /// <param name="precedence">Set where in the dictionary this key group will be ordered</param>
        /// <param name="userName">The User's Username</param>
        public String GenerateKey(String keyPart1, String keyPart2, String userName, int precedence)
        {
            String key = keyPart1 + "1" + keyPart2;

            if (Regex.Match(userName, "[0-9]+").Success)
                key += Regex.Match(userName, "[0-9]+").Value;

            key = String.Concat(Enumerable.Repeat("z", precedence)) + key;

            return key;
        }

    }




}
