import pandas as pd
import editdistance 

def merge():
    """Returns an openreview dataset after matching institution to its ranking"""
    
    df = pd.read_csv("openreview.csv", quotechar = '"')
    df = df.copy()
    r_1 = pd.read_csv("ranking_v2_david.csv", quotechar = '"')
    r_2 = pd.read_csv("ranking_v2_alex.csv", quotechar = '"')
    r_3 = pd.read_csv("ranking_v2_raymond.csv", quotechar = '"')
    r_4 = pd.read_csv("ranking_v2_keshav.csv", quotechar = '"')
    complete_df = ((r_1.append(r_2, ignore_index=True)) \
                   .append(r_3, ignore_index=True)) \
                   .append(r_4, ignore_index=True)
                   
    year_map = dict()
    for row in complete_df.iterrows():
        year = row[1]['year']
        institution = row[1]['institution']
        csranking = row[1]['csranking']
        ranking = row[1]['ranking']
        if year not in year_map:
            year_map[year] = dict()
        if institution not in year_map[year]:
            year_map[year][institution] = []
        year_map[year][institution] = dict({"csranking": csranking, "ranking": ranking})
    
    def add(ranking_type):
        def add_ranking_type(row):
            map_to_rank = year_map[row['year']]
            if not isinstance(row['institution'], str):
                return ""
            institutions = row['institution'].split(";")
            rankings = []
            for institution in institutions:
                if institution == "":
                    rankings.append(str(-1))
                    continue
                if institution in map_to_rank:
                    rankings.append(str(map_to_rank[institution][ranking_type]))
                else:
                    found = False
                    for existed_ranking in map_to_rank.keys():
                        if institution in existed_ranking \
                            or existed_ranking in institution \
                            or editdistance.eval(institution, existed_ranking) < 5:
                            rankings.append(str(map_to_rank[existed_ranking][ranking_type]))
                            found = True
                            break
                    if not found: 
                        rankings.append(str(-1))
            return ";".join(rankings)
        return add_ranking_type
        
    df['csranking'] = df.apply(add('csranking'), axis = 1)
    df['ranking'] = df.apply(add('ranking'), axis = 1)
    return df

if __name__ == "__main__":
    openreview = merge()
    openreview.to_csv("openreview.csv", index=False)
