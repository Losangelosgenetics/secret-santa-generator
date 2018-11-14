# Secret Santa Generator

A very simple Python script that randomly assignes a secret santa to a group of people, and sends an e-mail to all of the secret santa participants. You need Python 3 to run the script!

## Usage

1. Clone the repository via `git clone https://github.com/bokovhu/secret-santa-generator.git`
2. Run `pip install --upgrade google-api-python-client oauth2client`
3. Create a directory called `_env` in the directory you cloned the repository into
4. Head to https://developers.google.com/gmail/api/quickstart/python, and click the `ENABLE THE GMAIL API` button. A popup will appear, and you can download a JSON file via clicking `DOWNLOAD CLIENT CONFIGURATION`
5. Save the downloaded JSON file with the name `credentials.json` inside the `_env` directory
6. Create a file named `people` inside the `_env` directory
7. Add all of the secret santa participants inside this file. Each line in the file is a person, with the format `PERSON NAME <PERSON EMAIL>` (for example `John Doe <john.doe@mail.com>`)
8. Run `python secret-santa.py`, log into your Gmail account, and observe the Christmas miracle!