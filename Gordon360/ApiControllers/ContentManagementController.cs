﻿using Gordon360.Services;
using Gordon360.Repositories;
using Gordon360.Exceptions.ExceptionFilters;
using Gordon360.AuthorizationFilters;
using Gordon360.Static.Names;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Gordon360.Models.ViewModels;

namespace Gordon360.Controllers.Api
{
    [Route("api/cms")]
    [Authorize]
    [CustomExceptionFilter]
    public class ContentManagementController : ControllerBase
    {
        private readonly IContentManagementService _contentManagementService;

        public ContentManagementController()
        {
            var _unitOfWork = new UnitOfWork();
            _contentManagementService = new ContentManagementService(_unitOfWork);
        }

        public ContentManagementController(IContentManagementService contentManagementService)
        {
            _contentManagementService = contentManagementService;
        }

        /// <summary>Get all the slider content for the dashboard slider</summary>
        /// <returns>A list of all the slides for the slider</returns>
        /// <remarks>Queries the database for all entries in slider table</remarks>
        // GET: api/cms/slider
        [HttpGet]
        [Route("slider")]
        [AllowAnonymous]
        [StateYourBusiness(operation = Operation.READ_PUBLIC, resource = Resource.SLIDER)]
        public ActionResult<SliderViewModel> GetSliderContent()
        {
            var result = _contentManagementService.GetSliderContent();
            if (result == null)
            {
                return NotFound();
            }

            return Ok(result);
        }
    }
}
