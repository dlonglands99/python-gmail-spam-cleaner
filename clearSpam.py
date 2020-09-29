from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import oauth2client

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
service = None
target = 'SPAM'

def init(user_id = 'me', token_file = 'token.pickle', credentials_file = 'credentials.json'):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    deleteSpam(service, user_id)

def deleteSpam(service, user_id):
    messages = getMessages(service, user_id)

    if not messages:
        print('Spam is clear')
    else:
        service.users().messages().batchDelete(userId = user_id, body = messages).execute()
        print('Clearing spam folder')

def getMessages(service, user_id):
    results = service.users().messages().list(userId = 'me', labelIds = [target]).execute()
    messages = results.get('messages', [])
    return messages

if __name__ == '__main__':
    init()