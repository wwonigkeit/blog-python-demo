# This is an example of a script that collects Tweets based on a filter input and then identifies the language in the Tweet.
# The script is dependent on internet connectivity and also on the Google Cloud Translatio credentials files available from:
#
import json
import sys, getopt
from google.cloud import translate #required for the GCP Translation API
from google.oauth2 import service_account #required for the GCP Authentication API structure


def main(argv):
    gcpcreds_file = ''

    try:
        opts, args = getopt.getopt(argv,"m:g:",["message=","gcpcreds="])
    except getopt.GetoptError:
        print('get-lang.py -m <message> -g <gcp credentials file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('get-lang.py -m <message> -g <gcp credentials file>')
            sys.exit()
        elif opt in ("-m", "--message"):
            message = arg
        elif opt in ("-g", "--gcpcreds"):
            gcpcreds = arg

    try:
        gcpcreds_file = open(gcpcreds, 'r')
    except OSError:
        print("Could not open/read GCP credentials file:", inputfile)
        sys.exit()

    with gcpcreds_file:
        json_acct_info = json.load(gcpcreds_file)
    
    project_id = json_acct_info["project_id"]
    
    try:
        credentials = service_account.Credentials.from_service_account_info(json_acct_info)
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

        # Detecting the language of a text string
    
        client = translate.TranslationServiceClient(credentials=scoped_credentials)
        parent = f"projects/{project_id}/locations/global"

        response = client.detect_language(
            content=message,
            parent=parent,
            mime_type="text/plain",  # mime types: text/plain, text/html
        )
    except Exception as e:
        print("Google Translate API returned the following error:", e)
        sys.exit()

    dicts = {}
    # Display list of detected languages sorted by detection confidence.
    # The most probable language is first.
    for language in response.languages:
        dicts["langresult"] = [message, language.language_code, language.confidence]

    print(json.dumps(dicts))

if __name__ == "__main__":
   main(sys.argv[1:])
