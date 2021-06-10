class Credentials:
    def __init__(self, id, username, password=None):
        """
        Args:
            id (int): Account ID number
            username (str): Account username
            password (str): Account password
        """
        self.id = id
        self.username = username
        self.password = password

    def getID(self):
        """Return Gordon ID."""
        return self.id

    def getUsername(self):
        """Return username."""
        return self.username

    def getPassword(self):
        """Return password."""
        return self.password
