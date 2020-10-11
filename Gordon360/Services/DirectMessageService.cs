﻿using System;
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
    public class DirectMessageService : IDirectMessageService
    {


        public DirectMessageService()
        {
        }

        public bool CreateGroup(String id, String name, bool group, DateTime lastUpdated)
        {
            DateTime createdAt = DateTime.Now;

            var idParam = new SqlParameter("@_id", id);
            var nameParam = new SqlParameter("@name", name);
            var groupParam = new SqlParameter("@group", group);
            var createdAtParam = new SqlParameter("@createdAt", createdAt);
            var lastUpdatedParam = new SqlParameter("@lastUpdated", lastUpdated);
            var groupImageParam = new SqlParameter("@roomImage", null);

            var result = RawSqlQuery<WellnessViewModel>.query("CREATE_MESSAGE_ROOM @_id, @name, @group, @createdAt, @lastUpdated, @roomImage", idParam, nameParam, groupParam, createdAtParam, lastUpdatedParam, groupImageParam); //run stored procedure
            bool returnAnswer = true; 
            if (result == null)
            {
                returnAnswer = false;
                throw new ResourceNotFoundException() { ExceptionMessage = "The data was not found." };
            }



            return returnAnswer;

        }

        public bool SendMessage(String id, String room_id, String text, String user_id, bool system, bool sent, bool received, bool pending)
        {
            DateTime createdAt = DateTime.Now;
            var _unitOfWork = new UnitOfWork();
            var query = _unitOfWork.AccountRepository.FirstOrDefault(x => x.gordon_id == id);
            if (query == null)
            {
                throw new ResourceNotFoundException() { ExceptionMessage = "The account was not found." };
            }

            var idParam = new SqlParameter("@_id", id);
            var roomIdParam = new SqlParameter("@room_id", room_id);
            var textParam = new SqlParameter("@text", text);
            var createdAtParam = new SqlParameter("@createdAt", createdAt);
            var userIdParam = new SqlParameter("@user_id", user_id);
            var imageParam = new SqlParameter("@image", null);
            var videoParam = new SqlParameter("@video", null);
            var audioParam = new SqlParameter("@audio", null);
            var systemParam = new SqlParameter("@system", system);
            var sentParam = new SqlParameter("@sent", sent);
            var receivedParam = new SqlParameter("@received", received);
            var pendingParam = new SqlParameter("@pending", pending);

            var result = RawSqlQuery<WellnessViewModel>.query("INSERT_MESSAGE @_id, @room_id, @text, @createdAt,@user_id, @image, @video, @audio, @system, @sent, @received, @pending", 
                idParam, roomIdParam, textParam, createdAtParam, userIdParam, imageParam, videoParam, audioParam, systemParam, sentParam, receivedParam, pendingParam); //run stored procedure

            bool returnAnswer = true;
            if (result == null)
            {
                returnAnswer = false;
                throw new ResourceNotFoundException() { ExceptionMessage = "The data was not found." };
            }



            return returnAnswer;

        }

        public bool StoreUserRooms(String userId, String roomId)
        {
            var _unitOfWork = new UnitOfWork();
            var query = _unitOfWork.AccountRepository.FirstOrDefault(x => x.gordon_id == userId);
            if (query == null)
            {
                throw new ResourceNotFoundException() { ExceptionMessage = "The account was not found." };
            }

            var userIdParam = new SqlParameter("@user_id", userId);
            var roomIdParam = new SqlParameter("@room_id", roomId);
            

            var result = RawSqlQuery<WellnessViewModel>.query("INSERT_USER_ROOMS @user_id, @room_id", userIdParam, roomIdParam); //run stored procedure

            bool returnAnswer = true;

            if (result == null)
            {
                returnAnswer = false;
                throw new ResourceNotFoundException() { ExceptionMessage = "The data was not found." };
            }



            return returnAnswer;

        }


    }

}