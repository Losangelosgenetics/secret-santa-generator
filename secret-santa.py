import googleapiclient.discovery as gacd
import oauth2client as o2c
import oauth2client.file as o2cf
import oauth2client.tools as o2ct
import oauth2client.client as o2cc
import httplib2 as hl2
import os
import re
import email.mime.text
import base64
import random

OAUTH_SCOPES = 'https://mail.google.com/'

OAUTH_TOKEN_STORE_FILENAME = 'token.json'

"""
Visit https://developers.google.com/gmail/api/quickstart/python,
and click "ENABLE THE GMAIL API". You can download the JSON file
from the dialog.
"""
OAUTH_CREDENTIALS_FILENAME = '_env/credentials.json'

"""
People file example:
John Doe <john.doe@mail.com>
Jack Brown <jack.brown@mail.com>
Jane Smith <jane.smith@mail.com>
"""
PEOPLE_DATABASE_FILENAME = '_env/people'
PERSON_REGEX = '(?P<name>[a-zA-Z0-9 ]+)[<](?P<email>.*)[>]'

def authenticate ():

    oauthTokenStore = o2cf.Storage ('token.json')

    oauthCredentials = oauthTokenStore.get ()

    if not oauthCredentials or oauthCredentials.invalid:
        if not os.path.exists (OAUTH_CREDENTIALS_FILENAME) or not os.path.isfile (OAUTH_CREDENTIALS_FILENAME):
            raise FileNotFoundError (OAUTH_CREDENTIALS_FILENAME + ' does not exist!')

        oauthLoginFlow = o2cc.flow_from_clientsecrets (OAUTH_CREDENTIALS_FILENAME, OAUTH_SCOPES)
        oauthCredentials = o2ct.run_flow (oauthLoginFlow, oauthTokenStore)

    return oauthCredentials

def makeSecretSantaMail (senderEmailAddress, person, secretSantaOf):

    emailText = f"""
    Dear {person ["name"]},<br>
    You are the secret santa of {secretSantaOf ["name"]}.<br>
    <i>- Secret Santa Generator by Botond János Kovács &lt;botondjanoskovacs@gmail.com&gt;</i>
    """

    mimeMail = email.mime.text.MIMEText (emailText, 'html')

    mimeMail ['from'] = senderEmailAddress
    mimeMail ['to'] = f'{person ["name"]} <{person ["email"]}>'
    mimeMail ['subject'] = 'Secret Santa'

    return base64.urlsafe_b64encode ( mimeMail.as_bytes () ).decode ('utf8')

def readPeople ():
    people = []

    with open (PEOPLE_DATABASE_FILENAME, 'r') as peopleDatabaseFile:
        for line in peopleDatabaseFile:
            match = re.search (PERSON_REGEX, line)
            people.append ( { 'name': match.group ('name'), 'email': match.group ('email') } )

    return people

def main ():

    people = readPeople ()

    credentials = authenticate ()
    gmailService = gacd.build ('gmail', 'v1', http = credentials.authorize (hl2.Http ()))

    senderEmailAddress = gmailService.users ().getProfile (userId = 'me').execute () ['emailAddress']
    
    for i in range (1000):
        random.shuffle (people)

    for i in range (len (people)):

        thisPerson = people [i]
        secretSantaOf = people [(i + 1) % len (people)]

        gmailApiRequestData = {
            'raw': makeSecretSantaMail (senderEmailAddress, thisPerson, secretSantaOf)
        }

        messageSendResponse = gmailService.users ().messages ().send (userId = 'me', body = gmailApiRequestData).execute ()

if __name__ == '__main__':
    main ()