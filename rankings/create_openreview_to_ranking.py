import pandas as pd
import editdistance

def get_institutions_from_year(df, year):
    """Returns a set of unique institutions in a year"""
    df = df[df.year == year]
    institutions = set()
    for row in df.iterrows():
        row = row[1]
        if not isinstance(row.institution, str):
            continue
        for institution in row.institution.split(";"):
            if institution != "":
                institutions.add(institution)
    return institutions
    
def parse_csrankings(filename):
    csrankings = dict()
    with open(filename, "r") as infile:
        for i, line in enumerate(infile):
            if i == 0:
                continue
            
            processed = line.replace("piechart", "")
            processed = processed.replace("closed", "")
            processed = processed.replace("\n", "")
            processed = processed.split("\t")
            if len(processed) < 4:
                continue
            for i, element in enumerate(processed):
                processed[i] = element.strip()
            processed[0] = int(processed[0])
            processed[1] = processed[1][2:]
            csrankings[processed[1]] = processed[0]
    return csrankings
    
def parse_rankings(filename):
    def calculate_average(metrics):
        weights = [0.3, 0.3, 0.3, 0.025, 0.075]
        average = 0
        for metric, weight in zip(metrics[1:], weights):
            average += float(metric) * weight
        return round(average, 1)

    def calculate_rankings(scores, best_university):
        same_ranks = 0
        current_rank = 1
        current_score = scores[best_university]
        from operator import itemgetter
        sorted_ranking = sorted(scores.items(),key=itemgetter(1))
        new_ranking = dict()
        for uni, score in reversed(sorted_ranking):
            if score == current_score:
                new_ranking[uni] = current_rank
                same_ranks += 1
            else:
                current_rank += same_ranks
                current_score = score
                new_ranking[uni] = current_rank
                same_ranks = 1
        return new_ranking
        
    scores = dict()
    lines = []
    with open(filename, "r") as infile:
        for line in infile:
            lines.append(line)
            
    best_university = ""
    for i in range(2, len(lines), 3):
        university = lines[i].split("\t")[1].replace("\n", "")
        if i == 2:
            best_university = university
        metrics = lines[i + 2].split()
        scores[university] = calculate_average(metrics)
        
    return calculate_rankings(scores, best_university)

def create_csranking_map(institutions, csrankings):
    def smart_compare(s1, s2):
        return s1 in s2 or s2 in s1 or editdistance.eval(s1, s2) <= 2
    csranking_map = dict()
    for institution in institutions:
        if institution in csrankings:
            csranking_map[institution] = csrankings[institution]
            continue
        found = False
        for ranking in csrankings.keys():
            if smart_compare(institution, ranking):
                csranking_map[institution] = csrankings[ranking]
                found = True
                break
        if not found:
            csranking_map[institution] = -1
    return csranking_map

def build_csv(mapping):
    lines = []
    title = ["year", "institution", "csranking"]
    lines.append(title)
    for year in mapping.keys():
        for institution in mapping[year].keys():
            line = [year, institution, mapping[year][institution]]
            lines.append(line)
    return lines

def build_df(lines):
    df = pd.DataFrame(data=lines[1:], columns=lines[0])
    return df

def add_ranking(row):
    def get_similar(name, ranking_dataset):
        if name in ranking_dataset:
            return name 
        
        for key in ranking_dataset.keys():
            if name.lower() in key.lower():
                return key
            elif key.lower() in name.lower():
                return key
            elif editdistance.eval(key.lower(), name.lower()) <= 2:
                return key
        
        return ""
            
    ranking_dataset = rankings[row.year]
    key = get_similar(row['institution'], ranking_dataset)
    if key != "":
        return ranking_dataset[key]
    return -1

if __name__ == "__main__":
    openreview = pd.read_csv("openreview.csv", quotechar = '"')
    
    institutions = dict()
    for year in range(2017, 2021):
        institutions[year] = get_institutions_from_year(openreview, year)

    csrankings = dict()
    for year in range(2017, 2021):
        csrankings[year] = parse_csrankings(f"csrankings{year}.txt")
    
    rankings = dict()
    for year in range(2017, 2021):
        rankings[year] = parse_rankings(f"rankings{year}.txt")

    mapping = dict()
    for year in range(2017, 2021):
        mapping[year] = create_csranking_map(institutions[year], csrankings[year])

    df = build_df(build_csv(mapping))
    df['ranking'] = df.apply(add_ranking, axis = 1)
    df.to_csv("ranking_v2.csv", encoding='utf-8', index=False)
