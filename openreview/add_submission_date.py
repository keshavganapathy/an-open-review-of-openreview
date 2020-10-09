import pandas as pd
import pickle
import editdistance
import time

def add_submission_date():
    """Returns a dataset with submission date"""
    
    papers = None

    with open('papers.p', 'rb') as fp:
        papers = pickle.load(fp)

    openreview = pd.read_csv("openreview.csv", quotechar = '"')
    
    # create mapping from paper title to unix submission date
    tcdate = dict()
    for year in papers.keys():
        for key in papers[year].keys():
            paper_name = papers[year][key].content['title']
            date = papers[year][key].tcdate
            tcdate[paper_name] = time.strftime('%m/%d/%Y',  time.gmtime(date/1000.))
    
    def add_date(row):
        title = row['paper']
        if title in tcdate:
            return tcdate[title]
        else:
            for key in tcdate.keys():
                if not isinstance(key, str) or not isinstance(title, str):
                    continue
                if editdistance.eval(title, key) <= 13:
                    return tcdate[key]
                
    openreview['submission_date'] = openreview.apply(add_date, axis = 1)
    return openreview

if __name__ == "__main__":
    openreview = add_submission_date()
    openreview.to_csv("openreview.csv", index=False)
