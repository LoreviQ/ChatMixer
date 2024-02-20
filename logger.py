"""Contains the Logger class"""

import time

from gui import GUI


class Logger:
    """
    The Logger class takes a client and is passed to connections to various
    platforms. Serves as an abstraction for the logging.
    """

    def __init__(self, db=None, gui=None):
        self.db_client = db
        self.gui = gui

    def log_message(self, uname, platform, message):
        """
        If a db_client exists, adds message to the DB

        Args:
            uname: Username of the user (String)
            platform: Name of the platform (String)
            message: Contents of the message (String)
        """
        print(f"[{platform}] {uname}: {message}")
        if self.db_client:
            self.db_client.add_message(uname, platform, message)
        if self.gui:
            self.gui.add_line(f"[{platform}] {uname}: {message}")
