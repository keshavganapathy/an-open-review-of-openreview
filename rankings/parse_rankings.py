import pandas as pd

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

if __name__ == "__main__":
    for year in range(2017, 2021):
        rankings = parse_rankings(f"rankings{year}.txt")
        df = pd.DataFrame(rankings.items(), columns=['institution', 'ranking'])
        df.to_csv(f"parsed_rankings{year}.csv", encoding='utf-8', index=False)
