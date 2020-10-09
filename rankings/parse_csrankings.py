import pandas as pd

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

if __name__ == "__main__":
    # Parses csranking datasets of all years
    for year in range(2017, 2021):
        csrankings = parse_csrankings(f"csrankings{year}.txt")
        cs_df = pd.DataFrame(csrankings.items(), columns=['institution', 'csranking'])
        cs_df.to_csv(f"parsed_csrankings{year}.csv", encoding='utf-8', index=False)
