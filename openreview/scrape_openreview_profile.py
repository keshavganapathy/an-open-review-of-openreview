import openreview
import pandas as pd
import pickle

# sign in to Open Review
client = openreview.Client(baseurl='https://openreview.net',username="enter your username",password="enter your password")

def get_unique_emails(df):
    unique_emails = set()
    for emails in list(df['emails']):
        if isinstance(emails, str):
            for email in emails.split(";"):
                unique_emails.add(email)
    return unique_emails
    
def scrapeProfile(df):
    authors = dict()
    emails = get_unique_emails(df)
    for email in emails:
        try:
            profile = client.get_profile(email)
            authors[email] = profile
        except:
            continue
    return authors   

if __name__ == "__main__":
    df = pd.read_csv("openreview.csv", quotechar = '"')
    authors = scrapeProfile()
    with open('emails.p', 'wb') as fp:
        pickle.dump(authors, fp, protocol=pickle.HIGHEST_PROTOCOL)
 
    
