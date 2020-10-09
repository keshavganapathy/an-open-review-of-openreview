from __future__ import print_function
import openreview
import pandas as pd
import pickle

def parse_data():
    """Clean and parse raw data"""
    
    lines = []
    header = ("conference,year,paper,authors,"
              "emails,ratings,confidences,decisions,"
              "cmt_before_review,"
              "cmt_between,cmt_after_decision,double_blinded")
    lines.append(header)
    conference = "ICLR"

    def parse_score(line):
        return line.split(":")[0]

    for year in list(papers.keys()):
        for key in list(papers[year].keys()):
            # extract title, authors, and emails
            paper_content = papers[year][key].content
            title = paper_content['title']
            authors = ";".join(paper_content['authors'])
            emails = ";".join(paper_content['authorids'])
            ratings = ""
            confidences = ""
            decision = "Withdrawn"
            cmt_before_review = ""
            cmt_between = ""
            cmt_after_decision = ""
            
            # check if the confenrence is double blinded based on their website
            double_blinded = "no" if year == 2017 else "yes"
            
            if key in decisions[year]:
                # extract decision and decision date
                decision_content = decisions[year][key].content
                if year == 2019:
                    decision = decision_content['recommendation']
                    
                else:
                    decision = decision_content['decision']
                decision_date = decisions[year][key].tcdate
           
            if key in reviews[year]:
                # extract rating, confidence and first review date
                review_notes = reviews[year][key]
                ratings = []
                confidences = []
                review_date = -1
                for review in review_notes:
                    # first review date
                    if review_date == -1 or review.tcdate < review_date:
                        review_date = review.tcdate
                        
                    # rating
                    ratings.append(parse_score(review.content["rating"]))
                    
                    # confidence if exists
                    if "confidence" in review.content:
                        confidences.append(parse_score(review.content["confidence"]))
                        
                ratings = ";".join(ratings)
                confidences = ";".join(confidences)
                
                # extract comment before review, between review and decision,
                # and after decision
                cmt_before_review = 0
                cmt_between = 0
                if key in decisions[year]:
                    cmt_after_decision = 0
                
                for comments in [public_comments, official_comments]:
                    if year in comments and key in comments[year]:
                        for comment in comments[year][key]:
                            if comment.tcdate < review_date:
                                cmt_before_review += 1
                            elif key in decisions[year]:
                                if review_date < comment.tcdate < decision_date:
                                    cmt_between += 1
                                else:
                                    cmt_after_decision += 1
                            else:
                                if review_date < comment.tcdate:
                                    cmt_between += 1
            
            if decision == "Withdrawn":
                cmt_after_decision = ""
                
            line = (f"{conference},"
                    f"{year},"
                    f"\"{title}\","
                    f"\"{authors}\","
                    f"\"{emails}\","
                    f"{ratings},"
                    f"{confidences},"
                    f"\"{decision}\","
                    f"{cmt_before_review},"
                    f"{cmt_between},"
                    f"{cmt_after_decision},"
                    f"{double_blinded}")
            
            lines.append(line)
    return lines

if __name__ == "__main__":
    # import raw data
    papers, decisions, reviews = None, None, None
    public_comments, official_comments = None, None

    with open('papers.p', 'rb') as fp:
        papers = pickle.load(fp)

    with open('decisions.p', 'rb') as fp:
        decisions = pickle.load(fp)

    with open('reviews.p', 'rb') as fp:
        reviews = pickle.load(fp)

    with open('public_comments.p', 'rb') as fp:
        public_comments = pickle.load(fp)

    with open('official_comments.p', 'rb') as fp:
        official_comments = pickle.load(fp)
        
     # remove unecessary information that's not relevant to any of the existing papers
    for year in papers.keys():
        for key in list(decisions[year].keys()):
            if key not in papers[year]:
                del decisions[year][key]

        for key in list(reviews[year].keys()):
            if key not in papers[year]:
                del reviews[year][key]

        if year in public_comments:
            for key in list(public_comments[year].keys()):
                if key not in papers[year]:
                    del public_comments[year][key]

        if year in official_comments:
            for key in list(official_comments[year].keys()):
                if key not in papers[year]:
                    del official_comments[year][key]

    # 2018 has an extra decision
    del papers[2018]["ry5wc1bCW"]
    del decisions[2018]["ry5wc1bCW"]

    # parse data
    lines = parse_data()

    # export to a csv file
    with open("openreview.csv", "a") as f:
        for line in lines:
            f.write(line + "\n")
