import pandas as pd
import editdistance
import pickle

def create_paper_to_review(papers, reviews):
    """Returns a mapping from paper title to the corresponding review"""
    
    reviews_2020 = dict()
    for key in papers[2020].keys():
        title = papers[2020][key].content['title']
        reviews_2020[title] = []
        if key not in reviews[2020]:
            continue
        for review in reviews[2020][key]:
            paper_review = []
            for confidence in confidences:
                paper_review.append(review.content[confidence])
            reviews_2020[title].append(paper_review)
    return reviews_2020

def add_2020_review_assessment(df, reviews_2020):
    """Returns a new openreview dataset with combined textual reviews from the 2020 conference"""
    
    def parse(row):
        if row['year'] != 2020:
            return row['confidences']
        paper = row['paper']
        try:
            reviews = reviews_2020[paper]
            lst = []
            for review in reviews:
                lst.append(":".join(review))
            return ";".join(lst)
        except:
            # use editdistance to find papers with no exact match in title.
            # These errors usually come from papers with comma in the title resulting in error while reading the csv file.
            for key in reviews_2020.keys():
                if editdistance.eval(paper, key) <= 10:
                    reviews = reviews_2020[key]
                    lst = []
                    for review in reviews:
                        lst.append(":".join(review))
                    return ";".join(lst)
            return ""
    
    df['confidences'] = df.apply(parse, axis = 1)
    return df

if __name__ == "__main__":
    # import raw reviews and papers data
    reviews, papers = None, None

    with open('reviews.p', 'rb') as fp:
        reviews = pickle.load(fp)
        
    with open('papers.p', 'rb') as fp:
        papers = pickle.load(fp)

    # all possible confidences
    confidences = ['experience_assessment', \
                  'review_assessment:_checking_correctness_of_experiments', \
                  'review_assessment:_thoroughness_in_paper_reading', \
                  'review_assessment:_checking_correctness_of_derivations_and_theory' \
                 ]
    
    # add 2020 review assessment
    df = add_2020_review_assessment(pd.read_csv("openreview.csv"), create_paper_to_review(papers, reviews))
    df.to_csv("openreview.csv", encoding='utf-8', index=False)
