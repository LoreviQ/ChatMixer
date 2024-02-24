"""Contains class for Discord Bot"""

import asyncio
import os
import pickle
from datetime import datetime as dt

import google_auth_oauthlib.flow
import googleapiclient.discovery


class YoutubeBot:
    """
    Creates a bot to access Youtube API
    Uses local credentials.obj file to authenticate access
    If one does not exist, the user will be prompted to authenticate the app
    """

    def __init__(self, logger=None):
        self.platform = "Youtube"
        self.logger = logger
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.credentials = None
        self.livechatid = None
        self.lastchecked = None

        try:
            filehandler = open("credentials.obj", "rb")
            self.credentials = pickle.load(filehandler)
        except FileNotFoundError:
            self._get_credentials()

        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", credentials=self.credentials
        )

    def _get_credentials(self):
        """
        Called if credentials.obj does not exist
        Prompts the user to authenticate the app then saves the credentials
        """
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        client_secrets_file = "client_secret_340156162402-blmedvbod11dbmb4p5d8oomsb9nfpaom.apps.googleusercontent.com.json"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes
        )
        self.credentials = flow.run_console()

        filehandler = open("credentials.obj", "wb")
        pickle.dump(self.credentials, filehandler)

    def _get_livechat_id(self):
        """
        Gets the liveChatId of the latest broadcast of the authenticated user.
        This will be the current livechat if only one broadcast is made at a time.
        However, youtube allows multiple broadcasts.
        If you plan to use that feature this will need modifying.
        """
        request = self.youtube.liveBroadcasts().list(
            part="snippet,contentDetails,status", broadcastType="all", mine=True
        )
        response = request.execute()
        self.livechatid = response["items"][0]["snippet"]["liveChatId"]

    def _get_chat_messages(self):
        """
        Gets all the messages from a given livechat.
        """
        if not self.livechatid:
            self._get_livechat_id()
        request = self.youtube.liveChatMessages().list(
            liveChatId=self.livechatid, part="snippet,authorDetails"
        )
        response = request.execute()
        if response["pageInfo"]["totalResults"] > 0:
            return response["items"]
        return None

    def get_latest_messages(self):
        """
        Filteres the messages to only the latest messages and logs them
        """
        messages = self._get_chat_messages()
        if not messages:
            return
        dt_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        lastchecked = dt.strptime(messages[-1]["snippet"]["publishedAt"], dt_format)
        if self.lastchecked:
            messages = [
                m
                for m in messages
                if dt.strptime(m["snippet"]["publishedAt"], dt_format)
                > self.lastchecked
            ]
        self.lastchecked = lastchecked

        if self.logger:
            for message in messages:
                self.logger.log_message(
                    message["authorDetails"]["displayName"],
                    self.platform,
                    message["snippet"]["textMessageDetails"]["messageText"],
                    dt.strptime(message["snippet"]["publishedAt"], dt_format),
                )

    async def start(self):
        """
        Coroutine main function loop
        """
        while True:
            self.get_latest_messages()
            await asyncio.sleep(3)


if __name__ == "__main__":
    bot = YoutubeBot()
    bot.get_latest_messages()
