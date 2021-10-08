using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Xml.Linq;

namespace Gordon360.Models.ViewModels
{
    public class SearchResultViewModel
    {

        public static implicit operator SearchResultViewModel(EventViewModel evt)
        {
            SearchResultViewModel vm = new SearchResultViewModel()
            {
                QuickDesc = evt.Event_Name,
                SubDesc = evt.Event_Title,
                ShortDesc = evt.Event_Name,
                LongDesc = evt.Description,
                Type = "Event"
            };

            return vm;
        }

        public static implicit operator SearchResultViewModel(ActivityInfoViewModel act)
        {
            SearchResultViewModel vm = new SearchResultViewModel()
            {
                QuickDesc = act.ActivityDescription ?? act.ActivityDescription,
                SubDesc = null,
                ShortDesc = act.ActivityDescription,
                LongDesc = act.ActivityBlurb,
                Type = "Activity",
            };

            return vm;
        }

        public static implicit operator SearchResultViewModel(BasicInfoViewModel act)
        {
            SearchResultViewModel vm = new SearchResultViewModel()
            {
                QuickDesc = (act.Nickname != null ? act.Nickname : act.FirstName) + " " + act.LastName,
                SubDesc = act.UserName,
                ShortDesc = (act.Nickname != null ? act.Nickname : act.FirstName) + " " + act.LastName,
                LongDesc = "",
                Type = "Account",
            };

            return vm;
        }

        public string QuickDesc { get; set; }
        public string SubDesc { get; set; }
        public string ShortDesc { get; set; }
        public string LongDesc { get; set; }
        public string Type { get; set; }
        public int Precedence { get; set; }
    }
}
