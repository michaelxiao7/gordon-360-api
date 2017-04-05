﻿//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated from a template.
//
//     Manual changes to this file may cause unexpected behavior in your application.
//     Manual changes to this file will be overwritten if the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace Gordon360.Models
{
    using System;
    using System.Data.Entity;
    using System.Data.Entity.Infrastructure;
    using System.Data.Entity.Core.Objects;
    using System.Linq;
    
    public partial class CCTEntities1 : DbContext
    {
        public CCTEntities1()
            : base("name=CCTEntities1")
        {
        }
    
        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            throw new UnintentionalCodeFirstException();
        }
    
        public virtual DbSet<ADMIN> ADMIN { get; set; }
        public virtual DbSet<JNZB_ACTIVITIES> JNZB_ACTIVITIES { get; set; }
        public virtual DbSet<MEMBERSHIP> MEMBERSHIP { get; set; }
        public virtual DbSet<REQUEST> REQUEST { get; set; }
        public virtual DbSet<SUPERVISOR> SUPERVISOR { get; set; }
        public virtual DbSet<ACCOUNT> ACCOUNT { get; set; }
        public virtual DbSet<CM_SESSION_MSTR> CM_SESSION_MSTR { get; set; }
        public virtual DbSet<Faculty> Faculty { get; set; }
        public virtual DbSet<PART_DEF> PART_DEF { get; set; }
        public virtual DbSet<Staff> Staff { get; set; }
        public virtual DbSet<Student> Student { get; set; }
        public virtual DbSet<ACT_CLUB_DEF> ACT_CLUB_DEF { get; set; }
        public virtual DbSet<JENZ_ACT_CLUB_DEF> JENZ_ACT_CLUB_DEF { get; set; }
        public virtual DbSet<ACT_INFO> ACT_INFO { get; set; }
        public virtual DbSet<C360_SLIDER> C360_SLIDER { get; set; }
    
        public virtual ObjectResult<ACTIVE_CLUBS_PER_SESS_ID_Result> ACTIVE_CLUBS_PER_SESS_ID(string sESS_CDE)
        {
            var sESS_CDEParameter = sESS_CDE != null ?
                new ObjectParameter("SESS_CDE", sESS_CDE) :
                new ObjectParameter("SESS_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<ACTIVE_CLUBS_PER_SESS_ID_Result>("ACTIVE_CLUBS_PER_SESS_ID", sESS_CDEParameter);
        }
    
        public virtual ObjectResult<ALL_MEMBERSHIPS_Result> ALL_MEMBERSHIPS()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<ALL_MEMBERSHIPS_Result>("ALL_MEMBERSHIPS");
        }
    
        public virtual ObjectResult<ALL_REQUESTS_Result> ALL_REQUESTS()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<ALL_REQUESTS_Result>("ALL_REQUESTS");
        }
    
        public virtual ObjectResult<ALL_SUPERVISORS_Result> ALL_SUPERVISORS()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<ALL_SUPERVISORS_Result>("ALL_SUPERVISORS");
        }
    
        public virtual ObjectResult<LEADER_MEMBERSHIPS_PER_ACT_CDE_Result> LEADER_MEMBERSHIPS_PER_ACT_CDE(string aCT_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<LEADER_MEMBERSHIPS_PER_ACT_CDE_Result>("LEADER_MEMBERSHIPS_PER_ACT_CDE", aCT_CDEParameter);
        }
    
        public virtual ObjectResult<MEMBERSHIPS_PER_ACT_CDE_Result> MEMBERSHIPS_PER_ACT_CDE(string aCT_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<MEMBERSHIPS_PER_ACT_CDE_Result>("MEMBERSHIPS_PER_ACT_CDE", aCT_CDEParameter);
        }
    
        public virtual ObjectResult<MEMBERSHIPS_PER_MEMBERSHIP_ID_Result> MEMBERSHIPS_PER_MEMBERSHIP_ID(Nullable<int> mEMBERSHIP_ID)
        {
            var mEMBERSHIP_IDParameter = mEMBERSHIP_ID.HasValue ?
                new ObjectParameter("MEMBERSHIP_ID", mEMBERSHIP_ID) :
                new ObjectParameter("MEMBERSHIP_ID", typeof(int));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<MEMBERSHIPS_PER_MEMBERSHIP_ID_Result>("MEMBERSHIPS_PER_MEMBERSHIP_ID", mEMBERSHIP_IDParameter);
        }
    
        public virtual ObjectResult<MEMBERSHIPS_PER_STUDENT_ID_Result> MEMBERSHIPS_PER_STUDENT_ID(Nullable<int> sTUDENT_ID)
        {
            var sTUDENT_IDParameter = sTUDENT_ID.HasValue ?
                new ObjectParameter("STUDENT_ID", sTUDENT_ID) :
                new ObjectParameter("STUDENT_ID", typeof(int));
    
            var result = ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<MEMBERSHIPS_PER_STUDENT_ID_Result>("MEMBERSHIPS_PER_STUDENT_ID", sTUDENT_IDParameter);

            return result;
        }
    
        public virtual ObjectResult<REQUEST_PER_REQUEST_ID_Result> REQUEST_PER_REQUEST_ID(Nullable<int> rEQUEST_ID)
        {
            var rEQUEST_IDParameter = rEQUEST_ID.HasValue ?
                new ObjectParameter("REQUEST_ID", rEQUEST_ID) :
                new ObjectParameter("REQUEST_ID", typeof(int));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<REQUEST_PER_REQUEST_ID_Result>("REQUEST_PER_REQUEST_ID", rEQUEST_IDParameter);
        }
    
        public virtual ObjectResult<REQUESTS_PER_ACT_CDE_Result> REQUESTS_PER_ACT_CDE(string aCT_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<REQUESTS_PER_ACT_CDE_Result>("REQUESTS_PER_ACT_CDE", aCT_CDEParameter);
        }
    
        public virtual ObjectResult<REQUESTS_PER_STUDENT_ID_Result> REQUESTS_PER_STUDENT_ID(Nullable<int> sTUDENT_ID)
        {
            var sTUDENT_IDParameter = sTUDENT_ID.HasValue ?
                new ObjectParameter("STUDENT_ID", sTUDENT_ID) :
                new ObjectParameter("STUDENT_ID", typeof(int));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<REQUESTS_PER_STUDENT_ID_Result>("REQUESTS_PER_STUDENT_ID", sTUDENT_IDParameter);
        }
    
        public virtual ObjectResult<SUPERVISOR_PER_SUP_ID_Result> SUPERVISOR_PER_SUP_ID(Nullable<int> sUP_ID)
        {
            var sUP_IDParameter = sUP_ID.HasValue ?
                new ObjectParameter("SUP_ID", sUP_ID) :
                new ObjectParameter("SUP_ID", typeof(int));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<SUPERVISOR_PER_SUP_ID_Result>("SUPERVISOR_PER_SUP_ID", sUP_IDParameter);
        }
    
        public virtual ObjectResult<SUPERVISORS_PER_ACT_CDE_Result> SUPERVISORS_PER_ACT_CDE(string aCT_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<SUPERVISORS_PER_ACT_CDE_Result>("SUPERVISORS_PER_ACT_CDE", aCT_CDEParameter);
        }
    
        public virtual ObjectResult<EMAILS_PER_ACT_CDE_Result> EMAILS_PER_ACT_CDE(string aCT_CDE, string sESS_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            var sESS_CDEParameter = sESS_CDE != null ?
                new ObjectParameter("SESS_CDE", sESS_CDE) :
                new ObjectParameter("SESS_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<EMAILS_PER_ACT_CDE_Result>("EMAILS_PER_ACT_CDE", aCT_CDEParameter, sESS_CDEParameter);
        }
    
        public virtual ObjectResult<LEADER_EMAILS_PER_ACT_CDE_Result> LEADER_EMAILS_PER_ACT_CDE(string aCT_CDE, string sESS_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            var sESS_CDEParameter = sESS_CDE != null ?
                new ObjectParameter("SESS_CDE", sESS_CDE) :
                new ObjectParameter("SESS_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<LEADER_EMAILS_PER_ACT_CDE_Result>("LEADER_EMAILS_PER_ACT_CDE", aCT_CDEParameter, sESS_CDEParameter);
        }
    
        public virtual int SUPERVISORS_PER_ID_NUM(Nullable<int> iD_NUM)
        {
            var iD_NUMParameter = iD_NUM.HasValue ?
                new ObjectParameter("ID_NUM", iD_NUM) :
                new ObjectParameter("ID_NUM", typeof(int));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction("SUPERVISORS_PER_ID_NUM", iD_NUMParameter);
        }
    
        public virtual int UPDATE_ACT_CLUB_DEF()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction("UPDATE_ACT_CLUB_DEF");
        }
    
        public virtual int UPDATE_ACT_INFO()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction("UPDATE_ACT_INFO");
        }
    
        public virtual int UPDATE_JNZB_ACTIVITIES()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction("UPDATE_JNZB_ACTIVITIES");
        }
    
        public virtual ObjectResult<ADVISOR_EMAILS_PER_ACT_CDE_Result> ADVISOR_EMAILS_PER_ACT_CDE(string aCT_CDE, string sESS_CDE)
        {
            var aCT_CDEParameter = aCT_CDE != null ?
                new ObjectParameter("ACT_CDE", aCT_CDE) :
                new ObjectParameter("ACT_CDE", typeof(string));
    
            var sESS_CDEParameter = sESS_CDE != null ?
                new ObjectParameter("SESS_CDE", sESS_CDE) :
                new ObjectParameter("SESS_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<ADVISOR_EMAILS_PER_ACT_CDE_Result>("ADVISOR_EMAILS_PER_ACT_CDE", aCT_CDEParameter, sESS_CDEParameter);
        }
    
        public virtual ObjectResult<DISTINCT_ACT_TYPE_Result> DISTINCT_ACT_TYPE(string sESS_CDE)
        {
            var sESS_CDEParameter = sESS_CDE != null ?
                new ObjectParameter("SESS_CDE", sESS_CDE) :
                new ObjectParameter("SESS_CDE", typeof(string));
    
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<DISTINCT_ACT_TYPE_Result>("DISTINCT_ACT_TYPE", sESS_CDEParameter);
        }
    
        public virtual ObjectResult<string> CURRENT_SESSION()
        {
            return ((IObjectContextAdapter)this).ObjectContext.ExecuteFunction<string>("CURRENT_SESSION");
        }
    }
}
