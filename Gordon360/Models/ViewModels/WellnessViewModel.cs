﻿using System;
using System.Collections.Generic;
using System.Linq;

namespace Gordon360.Models.ViewModels
{
    public class WellnessViewModel
    {
        public string Status { get; set; }

        public DateTime Created { get; set; }

        public bool IsValid { get; set; }
    }
}