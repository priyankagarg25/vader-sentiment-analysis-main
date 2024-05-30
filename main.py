############################  
# Sentiment Analysis on Google Sheets with VADER using Python and Google Cloud Functions
# NOTE: This is the full Python code used and deployed in Google Cloud Functions as main.py

# VIEW THE POST ON MEDIUM: 
# https://towardsdatascience.com/sentiment-analysis-on-google-sheets-with-vader-using-python-and-google-cloud-functions-e767985ed27d
############################
 
# load all libraries
from googleapiclient.discovery import build
from google.oauth2 import service_account
import google.auth
from google.cloud import secretmanager
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
import numpy as np
import copy
import json
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# start of Cloud Function
def my_sentiment_function(request):      
    
    ############################  
    # Get the spreadsheet data 
    ############################

    # Specify the ID and relevant range of the spreadsheet
    SPREADSHEET_ID = 'your-spreadsheet-id' 
    GET_RANGE_NAME = 'your-range-name'
    

    # Authenticate Google Sheets
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    client = secretmanager.SecretManagerServiceClient()
    project_number = "your-project-number"
    secret_gsheet = "your-secret-name"
    secret_version_gsheet = "your-secret-version-number"
    secret_gsheet_name = f"projects/{project_number}/secrets/{secret_gsheet}/versions/{secret_version_gsheet}"
    secret_gsheet_value = client.access_secret_version(request={"name": secret_gsheet_name}).payload.data.decode("UTF-8")

    # Assign secret
    SERVICE_ACCOUNT_FILE = json.loads(secret_gsheet_value)

    # always specify creds as "None" first before setting it afterwards
    CREDS = None
    CREDS = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES) 


    # Now call the Sheets API    
    gsheet_service = build('sheets', 'v4', credentials = CREDS)
    sheet = gsheet_service.spreadsheets()
    result = sheet.values().get(spreadsheetId = SPREADSHEET_ID, range = GET_RANGE_NAME).execute()

    # get the data, otherwise return empty list
    feedback = result.get('values', []) 

    # assign headers which is always going to be row index 0
    feedback_headers = feedback.pop(0)

    # create a new dataframe with the headers
    feedback_df = pd.DataFrame(feedback, columns = feedback_headers)

    # view it
    print(feedback_df)


    ############################  
    # Run Sentiment Analysis
    ############################

    # create a deep copy of the df so we dont mess up the original df
    sentiment_df = copy.deepcopy(feedback_df)

    # set your stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))
    print(stop_words)

    # remove stop words from feedback column. Assign it to a new column called "feedback_without stopwords"
    sentiment_df['feedback_without_stopwords'] = sentiment_df['Feedback'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))

    # view df
    print(sentiment_df)

    # now load vader
    nltk.download('vader_lexicon')

    # get the vader sentiment intensity analyser
    the_force = SentimentIntensityAnalyzer()

    # apply onto column in df where stopwords have been removed from feedback
    sentiment_df['polarity_scores'] = sentiment_df['feedback_without_stopwords'].apply(the_force.polarity_scores)

    # view df
    print(sentiment_df)


    # get the compound scores only, round to 2 decimals
    compound_scores = [round(the_force.polarity_scores(i)['compound'], 2) for i in sentiment_df['feedback_without_stopwords']]

    # now create new column in the dataframe and save compound scores in it
    sentiment_df['compound_scores'] = compound_scores

    # view df
    print(sentiment_df)

    # create simple logic
    sent_logic = [
        (sentiment_df['compound_scores'] < 0),
        (sentiment_df['compound_scores'] >= 0) & (sentiment_df['compound_scores'] < 0.5),
        (sentiment_df['compound_scores']  >= 0.5)
        ]

    sent_summary = ['negative', 'neutral', 'positive']

    # assign to a new column
    sentiment_df['sentiment'] = np.select(sent_logic, sent_summary)

    # view df
    print(sentiment_df)


    ############################  
    # Write results to a new sheet
    ############################


    # using gspread, reference the Google Sheets credentials from earlier
    gc = gspread.authorize(CREDS)

    # Specify the google spreadsheet
    get_the_sheet = gc.open_by_key(SPREADSHEET_ID)

    # Specify the name of the specific tab this data is to be written to. 
    write_to_tab = get_the_sheet.worksheet('Sheet2')

    # clear anything existing in current tab in sheet
    write_to_tab.clear()


    # write it
    set_with_dataframe(worksheet = write_to_tab, dataframe = sentiment_df, include_index = False, include_column_header = True, resize = True)
    




    # then finally:     
    return "Yay! Done!"
  


############################  
# END
############################
