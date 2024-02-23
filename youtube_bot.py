"""Contains class for Discord Bot"""

import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery


class YoutubeBot:
    """
    Creates a subclass of the discord.Client class
    Initialises the bot based on .env variables
    """

    def __init__(self, logger=None):
        self.platform = "Youtube"
        self.logger = logger
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.credentials = None
        self.livechatid = None

        try:
            filehandler = open("credentials.obj", "rb")
            self.credentials = pickle.load(filehandler)
        except:
            self._get_credentials()

        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", credentials=self.credentials
        )

    def _get_credentials(self):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        client_secrets_file = "client_secret_340156162402-blmedvbod11dbmb4p5d8oomsb9nfpaom.apps.googleusercontent.com.json"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes
        )
        self.credentials = flow.run_console()

        filehandler = open("credentials.obj", "wb")
        pickle.dump(self.credentials, filehandler)

    def _get_livechat_id(self):
        request = self.youtube.liveBroadcasts().list(
            part="snippet,contentDetails,status", broadcastType="all", mine=True
        )
        response = request.execute()
        self.livechatid = response["items"][0]["snippet"]["liveChatId"]

    def _get_chat_messages(self):
        if not self.livechatid:
            self._get_livechat_id()
        request = self.youtube.liveChatMessages().list(
            liveChatId=self.livechatid, part="snippet,authorDetails"
        )
        response = request.execute()
        print(response)

    async def on_ready(self):
        """Method called when the Bot has successfully connected"""
        print(f"Connected to {self.platform} as: ")

    async def on_message(self, message):
        """
        Method called upon any message, logs the message

        Args:
            message: ~
        """
        pass


if __name__ == "__main__":
    bot = YoutubeBot()
    bot._get_chat_messages()
