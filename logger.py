"""Contains the Logger class"""

from datetime import datetime as dt


class Logger:
    """
    The Logger class takes a client and is passed to connections to various
    platforms. Serves as an abstraction for the logging.
    """

    def __init__(self, db=None, gui=None):
        self.db_client = db
        self.gui = gui

    def log_message(self, uname, platform, message, timestamp=dt.now()):
        """
        Adds message to the DB and pushes message to GUI

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)
            message: Contents of the message (String)
            timestamp: Time the message was sent. (Optional)
        """
        print(f"[{platform}] {uname}: {message} - {timestamp}")
        if self.db_client:
            self.db_client.add_message(uname, platform, message, timestamp)
        if self.gui:
            self.gui.add_line(f"[{platform}] {uname}: {message}")
