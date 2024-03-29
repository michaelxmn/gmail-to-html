import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class GmailConnection:
  def __init__(self, credentials_file):
    self.credentials_file = credentials_file

  def connect(self):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_file, SCOPES
        )
        creds = flow.run_local_server(port=5001, redirect_uri_trailing_slash=False)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

    return service
