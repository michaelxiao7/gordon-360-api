class Credentials:
    """Class to store and retrieve credentials for HTTP authentication. """
    def __init__(self, id_number, username, password=None, token=None):
        """
        Args:
            id_number (int): Account ID number.
            username (str): Account username.
            password (str): Account password.
            token (str): Temporary API token.
        """
        self.id_number = id_number
        self.username = username
        self.password = password
        self.token = token

    def getID(self):
        """Return Gordon ID."""
        return self.id_number

    def getUsername(self):
        """Return username."""
        return self.username

    def getPassword(self):
        """Return password."""
        return self.password

    def getToken(self):
        """Return token."""
        return self.token
    
    def setPassword(self, password=None):
        """Set password.  If not supplied then prompt for new password."""
        from getpass import getpass
        if password is None:
            self.password = getpass()
        else:
            self.password = password

    def setToken(self, token):
        """Set token."""
        self.token = token
