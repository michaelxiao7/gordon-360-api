﻿using System;
using System.Collections.Generic;
using System.Xml.Linq;
using System.Linq;


namespace Gordon360.Models.ViewModels
{

    public class DEPRECATED_EventViewModel
    {
        // Class element declarations
        public string Event_ID { get; set; }
        public string Event_Name { get; set; }
        public string Event_Title { get; set; }
        public string Event_Type_Name { get; set; }
        public bool HasCLAWCredit { get; set; }
        public bool IsPublic { get; set; }
        public string Description { get; set; }
        public List<EventOccurence> Occurrences { get; set; }
        public string Organization { get; set; }

        // Set the namespace for X Paths
        private readonly XNamespace r25 = "http://www.collegenet.com/r25";

        // This view model contains pieces of info pulled from a JSon array which is pulled from 25Live, using a pre-defined function
        public DEPRECATED_EventViewModel(XElement a)
        {
            Event_ID = a.Element(r25 + "event_id")?.Value;
            Event_Name = a.Element(r25 + "event_name")?.Value;
            Event_Title = a.Element(r25 + "event_title")?.Value;
            Event_Type_Name = a.Element(r25 + "event_type_name")?.Value;
            Description = a.Elements(r25 + "event_text")?.FirstOrDefault(t => t.Element(r25 + "text_type_id")?.Value == "1")?.Element(r25 + "text")?.Value;
            Organization = a.Element(r25 + "organization")?.Element(r25 + "organization_name")?.Value;
            HasCLAWCredit = a.Elements(r25 + "category")?.Any(c => c.Element(r25 + "category_id")?.Value == "85") ?? false;
            IsPublic = a.Elements(r25 + "requirement")?.Any(r => r.Element(r25 + "requirement_id")?.Value == "3") ?? false;

            Occurrences = a.Element(r25 + "profile")?.Descendants(r25 + "reservation").Select(o => new EventOccurence
            {
                StartDate = o.Element(r25 + "event_start_dt")?.Value,
                EndDate = o.Element(r25 + "event_end_dt")?.Value,
                Location = o.Element(r25 + "space_reservation")?.Element(r25 + "space")?.Element(r25 + "formal_name")?.Value
            }).ToList();
        }

        /// <summary>
        /// Initializes a new custom instance of the <see cref="DEPRECATED_EventViewModel"/> class.
        /// </summary>
        public DEPRECATED_EventViewModel(DEPRECATED_EventViewModel baseEvent, EventOccurence occurrence)
        {
            this.Event_ID = $"{baseEvent.Event_ID}_{occurrence.GetHashCode()}";
            this.Event_Name = baseEvent.Event_Name;
            this.Event_Title = baseEvent.Event_Title;
            this.Event_Type_Name = baseEvent.Event_Type_Name;
            this.Description = baseEvent.Description;
            this.Organization = baseEvent.Organization;
            this.IsPublic = baseEvent.IsPublic;
            this.HasCLAWCredit = baseEvent.HasCLAWCredit;
            this.Occurrences = new List<EventOccurence> { occurrence };
        }
    }


    public class EventOccurence
    {
        public string StartDate { get; set; }
        public string EndDate { get; set; }
        public string Location { get; set; }
    }

}