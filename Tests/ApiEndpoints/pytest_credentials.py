from Credentials import Credentials

# Test accounts.  These are valid Active Directory (AD) accounts in Gordon's
# AD Domain but are only used for testing Gordon360.
student = Credentials(999999097, "360.studenttest", "Matthew28!!")
staff   = Credentials(999999098, "360.stafftest",   "Matthew28!!")
faculty = Credentials(999999099, "360.facultytest", "Matthew28!!")

# Map the test accounts to various user roles in Gordon360, particularly for
# Involvements (aka Activities).  
member = student    # 2021-06-30: 360.student test has facstaff college role
leader = faculty
advisor = faculty
groupadmin = faculty
superadmin = staff

# Involvements Testing 
username = member.getUsername()
password = member.getPassword()
id_number = member.getID()

username_activity_leader = leader.getUsername()
password_activity_leader = leader.getPassword()
id_number_activity_leader = leader.getID()

username_superadmin = superadmin.getUsername()
password_superadmin = superadmin.getPassword()
id_number_superadmin = superadmin.getID()
