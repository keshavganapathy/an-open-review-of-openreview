from __future__ import print_function
import openreview
import pandas as pd
import pickle

# sign in openreview.net
client = openreview.Client(baseurl='https://openreview.net',username="create your own account",password="create your own password")

def scrapePapers():
    """Scrapes all papers from ICLR conference from 2017 - 2020 including withdrawn ones"""
    
    papers_invi = {2017: "ICLR.cc/2017/conference/-/submission", \
                   2018: "ICLR.cc/2018/Conference/-/Blind_Submission", \
                   2019: "ICLR.cc/2019/Conference/-/Blind_Submission", \
                   2020: "ICLR.cc/2020/Conference/-/Blind_Submission"}
                   
    papers = dict()
    for year in papers_invi.keys():
        papers[year] = {note.forum: note for note in openreview.tools.iterget_notes(client, invitation=papers_invi[year])}
        
    papers_invi = {2017: "ICLR.cc/2017/Conference/-/Withdrawn_Submission", \
        2018: "ICLR.cc/2018/Conference/-/Withdrawn_Submission", \
        2019: "ICLR.cc/2019/Conference/-/Withdrawn_Submission", \
        2020: "ICLR.cc/2020/Conference/-/Withdrawn_Submission"}
        
    for year in papers_invi.keys():
        for note in openreview.tools.iterget_notes(client, invitation=papers_invi[year]):
            papers[year][note.forum] = note
            
    return papers

def scrapeDecisions():
    """Scrapes all decisions relesased from ICLR conference from 2017 - 2020"""
    
    decisions_invi = {2017: 'ICLR.cc/2017/conference/-/paper.*/acceptance', \
                      2018: "ICLR.cc/2018/Conference/-/Acceptance_Decision", \
                      2019: 'ICLR.cc/2019/Conference/-/Paper.*/Meta_Review', \
                      2020: "ICLR.cc/2020/Conference/Paper.*/-/Decision"}
                      
    decisions = dict()
    for year in decisions_invi.keys():
        decisions[year] = {note.forum: note for note in openreview.tools.iterget_notes(client, invitation=decisions_invi[year])}
        
    return decisions

def scrapeReviews():
    """Scrapes all reviews relesased from ICLR conference from 2017 - 2020"""

    reviews_invi = {2017: "ICLR.cc/2017/conference/-/paper.*/official/review", \
                    2018: "ICLR.cc/2018/Conference/-/Paper.*/Official_Review", \
                    2019: "ICLR.cc/2019/Conference/-/Paper.*/Official_Review", \
                    2020: "ICLR.cc/2020/Conference/Paper.*/-/Official_Review"}
                    
    reviews = dict()    
    for year in reviews_invi.keys():
        for note in openreview.tools.iterget_notes(client, invitation=reviews_invi[year]):
            if note.forum in reviews[year]:
                reviews[year][note.forum].append(note)
            else:
                reviews[year][note.forum] = [note]
                
    return reviews

def scrapePublicComments():
    """Scrapes all public comments from ICLR conference from 2017 - 2019"""
    
    public_comments_invi = {2017: 'ICLR.cc/2017/conference/-/paper.*/public/comment', \
                            2018: 'ICLR.cc/2018/Conference/-/Paper.*/Public_Comment', \
                            2019: 'ICLR.cc/2019/Conference/-/Paper.*/Public_Comment'}
                            
    public_comments = dict()
    for year in public_comments_invi.keys():
        public_comments[year] = dict()
        invi = public_comments_invi[year]
        for note in openreview.tools.iterget_notes(client, invitation=invi):
            if note.forum in public_comments[year]:
                public_comments[year][note.forum].append(note)
            else:
                public_comments[year][note.forum] = [note]
                
    return public_comments

def scrapeOfficialComments():
    """Scrapes all official comments from ICLR conference from 2018 - 2020"""

    official_comments_invi = {2018: 'ICLR.cc/2018/Conference/-/Paper.*/Official_Comment', \
                              2019: 'ICLR.cc/2019/Conference/-/Paper.*/Official_Comment', \
                              2020: 'ICLR.cc/2020/Conference/Paper.*/-/Official_Comment'}
                              
    official_comments = dict()
    for year in list(official_comments_invi.keys()):
        official_comments[year] = dict()
        invi = official_comments_invi[year]
        for note in openreview.tools.iterget_notes(client, invitation=invi):
            if note.forum in official_comments[year]:
                official_comments[year][note.forum].append(note)
            else:
                official_comments[year][note.forum] = [note]
                
    return official_comments
    
if __name__ == "__main__":
    papers  = scrapePapers()
    decisions = scrapeDecisions()
    reviews = scrapeReviews()
    public_comments = scrapePublicComments()
    official_comments = scrapeOfficialComments()

    # save data
    with open('papers.p', 'wb') as fp:
       pickle.dump(papers, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('decisions.p', 'wb') as fp:
       pickle.dump(decisions, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('reviews.p', 'wb') as fp:
       pickle.dump(reviews, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('public_comments.p', 'wb') as fp:
       pickle.dump(public_comments, fp, protocol=pickle.HIGHEST_PROTOCOL)
     
    with open('official_comments.p', 'wb') as fp:
       pickle.dump(official_comments, fp, protocol=pickle.HIGHEST_PROTOCOL)
