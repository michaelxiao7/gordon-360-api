using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Gordon360.Models;
using Gordon360.Models.ViewModels;
using Gordon360.Repositories;
using Gordon360.Exceptions.CustomExceptions;
using System.Data.SqlClient;
using Gordon360.Services.ComplexQueries;
using System.Diagnostics;

namespace Gordon360.Services
{
    public class HousingService : IHousingService
    {
        private IUnitOfWork _unitOfWork;


        public HousingService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        /// <summary>
        /// Gets student housing info
        /// TODO list what exactly we mean by houding info
        /// </summary>
        /// <returns>The housing item</returns>
        public IEnumerable<HousingViewModel> GetAll()
        {
            return RawSqlQuery<HousingViewModel>.query("GET_STU_HOUSING_INFO");
        }

        public string GetApplicationID(string username)
        {
            var idParam = new SqlParameter("@MODIFIER_ID", username);
            var query = RawSqlQuery<string>.query("GET_AA_APPID_BY_NAME @MODIFIER_ID", idParam); //run stored procedure
            var applicationID = query.FirstOrDefault();
            return applicationID;
        }

        /// <summary>
        /// Saves student housing info
        /// - first, it creates a new row in the applications table and puts the id of the primary applicant and a timestamp
        /// - second, it looks for the application id of the application with the information we just input (because 
        /// the database creates the application ID so we have to ask it which number it generated for it)
        /// - third, it inserts each applicant into the applicnts table along with the apartment ID so we know
        /// which application on which they are an applicant
        ///  
        /// </summary>
        /// <returns>Whether or not all the queries succeeded</returns>
        public bool SaveApplication(string modifierId, string sess_cde, string [] appIds)
        {
            IEnumerable<ApartmentAppSaveViewModel> result = null;
            IEnumerable<ApartmentAppIDViewModel> idResult = null;
            IEnumerable<ApartmentApplicantViewModel> result2 = null;

            DateTime now = System.DateTime.Now;

            var timeParam = new SqlParameter("@NOW", now);
            var modParam = new SqlParameter("@MODIFIER_ID", modifierId);
            var sessionParam = new SqlParameter("@SESS_CDE", sess_cde);

            bool returnAnswer = true;

            result = RawSqlQuery<ApartmentAppSaveViewModel>.query("INSERT_AA_APPLICATION @NOW, @MODIFIER_ID", timeParam, modParam); //run stored procedure
            if (result == null)
            {
                returnAnswer = false;
                throw new ResourceNotFoundException() { ExceptionMessage = "The application could not be saved." };
            }

            // The following is ODD, I know. It seems you cannot execute the same query with the same sql parameters twice.
            // Thus, these two sql params must be recreated after being used in the last query:

            timeParam = new SqlParameter("@NOW", now);
            modParam = new SqlParameter("@MODIFIER_ID", modifierId);

            idResult = RawSqlQuery<ApartmentAppIDViewModel>.query("GET_AA_APPID_BY_NAME_AND_DATE @NOW, @MODIFIER_ID", timeParam, modParam); //run stored procedure
            if (idResult == null)
            {
                returnAnswer = false;
                throw new ResourceNotFoundException() { ExceptionMessage = "The new application ID could not be found." };
            }

            ApartmentAppIDViewModel idModel = idResult.ElementAt(0);

            SqlParameter appIdParam = null;
            SqlParameter idParam = null;
            SqlParameter programParam = null;

            foreach (string id in appIds) {
                // this constructs new SqlParameters each time we iterate (despite that only 1/4 will actually be different
                // on subsequent iterations. See above explanation of this ODD strategy.

                //idParam.Value = id; might need if this ODD solution is not satisfactory
                appIdParam = new SqlParameter("@APPLICATION_ID", idModel.AprtAppID);
                idParam = new SqlParameter("@ID_NUM", id);
                programParam = new SqlParameter("@APRT_PROGRAM", "");
                sessionParam = new SqlParameter("@SESS_CDE", sess_cde);

                result2 = RawSqlQuery<ApartmentApplicantViewModel>.query("INSERT_AA_APPLICANT @APPLICATION_ID, @ID_NUM, @APRT_PROGRAM, @SESS_CDE", appIdParam, idParam, programParam, sessionParam); //run stored procedure
                if (result2 == null)
                {
                    returnAnswer = false; // not sure if this matters since I have heard throwing an exception "returns"
                    throw new ResourceNotFoundException() { ExceptionMessage = "Applicant with ID " + id + " could not be saved." };   
                }
            }
             
            return returnAnswer;
        }
    }
}
