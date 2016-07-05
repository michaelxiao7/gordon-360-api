﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using CCT_App.Models;
using CCT_App.Models.ViewModels;
using CCT_App.Repositories;

namespace CCT_App.Services
{
    /// <summary>
    /// Service class that facilitates data passing between the ParticipationsController and the database model.
    /// </summary>
    public class ParticipationService : IParticipationService
    {
        private IUnitOfWork _unitOfWork;

        public ParticipationService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        /// <summary>
        /// Fetches the participation record whose id matches the given parameter.
        /// </summary>
        /// <param name="id">The participation id.</param>
        /// <returns>If found, returns ParticipationViewModel, if not returns null.</returns>
        public ParticipationViewModel Get(string id)
        {
            var query = _unitOfWork.ParticipationRepository.GetById(id);
            ParticipationViewModel result = query;
            return result;
        }
        /// <summary>
        /// Fetches all the participation records from the database
        /// </summary>
        /// <returns>Participation IEnumerable. If no records are found, returns an empty IEnumberable</returns>
        public IEnumerable<ParticipationViewModel> GetAll()
        {
            var query = _unitOfWork.ParticipationRepository.GetAll();
            var result = query.Select<PART_DEF, ParticipationViewModel>(x => x);
            return result;
        }
    }
}