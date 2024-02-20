"""Contains the Logger class"""


class Logger:
    """
    The Logger class takes a client and is passed to connections to various
    platforms. Serves as an abstraction for the logging.
    """

    def __init__(self, client=None):
        self.db_client = client

    def log_message(self, uname, platform, message):
        """
        If a db_client exists, adds message to the DB

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)
            message: Contents of the message (String)
        """
        if self.db_client:
            self.db_client.add_message(uname, platform, message)
