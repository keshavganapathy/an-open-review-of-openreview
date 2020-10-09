import pandas as pd
import editdistance
import pickle

def get_abstract(papers):
    abstract = dict({2017:{}, 2018:{}, 2019:{}, 2020:{}})
    for year in papers.keys():
        for paper_key in papers[year].keys():
            title = papers[year][paper_key].content['title'].strip()
            abstract[year][title] = papers[year][paper_key].content['abstract'].lower()
    return abstract

def get_tldr(papers):
    tldr = dict({2017:{}, 2018:{}, 2019:{}, 2020:{}})
    for year in papers.keys():
        for paper_key in papers[year].keys():
            title = papers[year][paper_key].content['title'].strip()
            if 'TL;DR' in papers[year][paper_key].content:
                tldr[year][title] = papers[year][paper_key].content['TL;DR'].lower()
            else:
                tldr[year][title] = ""
    return tldr

def get_keyword(papers):
    keyword = dict({2017:{}, 2018:{}, 2019:{}, 2020:{}})
    for year in papers.keys():
        for paper_key in papers[year].keys():
            title = papers[year][paper_key].content['title'].strip()
            keyword[year][title] = " ".join(papers[year][paper_key].content['keywords']).lower()
    return keyword
    
def add_categories(df, abstract, tldr, keyword):
    D = {'theorem': 1,
         ' prove ': 1,
         'proof': 1,
         ' bound ': 1,
         'computer vision': 2,
         'object detection': 2,
         'segmentation': 2,
         'pose estimation': 2,
         'optical character recognition': 2,
         'structure from motion': 2,
         'facial recognition': 2,
         'face recognition': 2,
         'natural language processing': 3,
         'nlp': 3,
         'named-entity': 3,
         'word embeddings': 3,
         'part-of-speech': 3,
         'natural language': 3,
         'named-entity recognition': 3,
         'machine translation': 3,
         'language model': 3,
         'adversarial': 4,
         'attack': 4,
         'poison': 4,
         'adversarial example': 4,
         'adversarially roburst': 4,
         'adversarial training': 4,
         'certified roburst': 4,
         'certifiably roburst': 4,
         'backdoor': 4,
         'generative adversarial network': 5,
         'generative': 5,
         ' gan': 5,
         '(gan': 5,
         'variational autoencoder': 5,
         'vae': 5,
         'few-shot': 6,
         'meta-learning': 6,
         'transfer learning': 6,
         'zero-shot': 6,
        'fairness': 7,
         'gender': 7,
          'racial': 7,
        'racist': 7,
        'unfair': 7,
        'demographic': 7,
        'ethnic': 7,
        'generalization': 8,
        'optimization theory': 9,
        'convergence rate': 9,
        'convex optimization': 9,
        'rate of convergence': 9,
        'global convergence': 9,
        'local convergence': 9,
        'stationary point': 9,
        ' graph': 10,
        'bayesian': 11}

    df = df.copy()
    no = set()

    def add_categories_helper(row):
        nonlocal no
        if not isinstance(row['paper'], str):
            return ""
        
        categories = []
        title = row['paper'].strip()
        if title not in abstract[row['year']]:
            no.add((row['year'], title))
            return ""
        abstract_paper = abstract[row['year']][title]
        tldr_paper = tldr[row['year']][title]
        keyword_paper = keyword[row['year']][title]
        for category in D.keys():
            if category in abstract_paper or category in tldr_paper:
                categories.append(str(D[category]))
        return ";".join(list(set(categories)))


    df['categories'] = df.apply(add_categories_helper, axis=1)

    def add_rest(row):
        if not isinstance(row['paper'], str):
            return ""
        if (row['year'], row['paper']) not in no:
            return row['categories']
        
        categories = []
        title = row['paper'].strip()
        year = row['year']
        for key in abstract[year].keys():
            if editdistance.eval(key, title) < 8:
                title = key
                break
        abstract_paper = abstract[row['year']][title]
        tldr_paper = tldr[row['year']][title]
        keyword_paper = keyword[row['year']][title]
        for category in D.keys():
            if category in abstract_paper or category in tldr_paper:
                categories.append(str(D[category]))
        return ";".join(list(set(categories)))

    df['categories'] = df.apply(add_rest, axis = 1)
    return df

if __name__ == "__main__":

    # load csv dataset
    df = pd.read_csv("openreview.csv")
    
    # load raw paper data
    papers = None

    with open("papers.p", 'rb') as fp:
        papers = pickle.load(fp)
        
    # add categories to paper using keyword
    abstract = get_abstract(papers)
    tldr = get_tldr(papers)
    keyword = get_keyword(papers)
    new_df = add_categories(df, abstract, tldr, keyword)
    new_df.to_csv("openreview.csv")
        
    
