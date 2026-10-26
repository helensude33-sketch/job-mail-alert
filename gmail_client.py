import os # check if file exists or not. (file= token.json)
from google.auth.transport.requests import Request # refreshes the expired token
from google.oauth2.credentials import Credentials #reads the saved token
from google_auth_oauthlib.flow import InstalledAppFlow #on first login opens the browser and gets permission
from googleapiclient.discovery import build #creates the ready remote control to talk to the gmail API

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"] #mail read permission requested from google

def get_gmail_service():
    creds = None #we don't have login info

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        #If logged in before, there is a token. Read it

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        #if expired but there is a refresh key, refresh without asking the user
        else: 
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0) 
            #if never logged in, the login screen opens in the browser with credentials.json and permission is given
        
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
            #saves the new token to the file
                   
    return build("gmail", "v1", credentials=creds)
    #creates the object that talks to version 1 of the gmail api and returns it


def list_recent_emails(service, max_results=10):
    result = service.users().messages().list(userId="me", maxResults=max_results).execute()
    #asks for the IDs of the last 10 mails from mail

    messages = result.get("messages", [])
    #get the message list, if there is none use an empty list
    emails = [] 

    for msg in messages:
        full = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject"]
        ).execute()
        #mail info

        headers = {h["name"]: h["value"] for h in full["payload"]["headers"]}
        #gives the mail headers as a list, convert to a dictionary

        emails.append({ #add this mail to the list in an organised way 
            "id": msg["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "snippet": full.get("snippet", ""),
        })

    return emails #return the organised mail list

if __name__ == "__main__":
    service = get_gmail_service()
    for email in list_recent_emails(service):
        print(email["from"], "|", email["subject"])
        #works with python gmail_client.py. Doesn't work if someone else imports it. Logs in, gets the last 10 mails. Writes from-subject etc. to the screen