import csv
import sys
import pandas as pd



#inFile must be a raw text file copying all sidekick clan feed
def extract_activity_sikekick(inFile, outFile):
    activities={}
    data = pd.read_csv(inFile, header=0, delimiter=',', quoting=0, encoding="utf-8",
                           ).fillna("none")
    data=data.values

    for row in data:
        msg= row[3]

        if " upgrade" in msg or " push" in msg:
            lines=msg.split("\n")

            for l in lines:
                if " upgrade" not in l and "push" not in l:
                    continue

                s = l.index(" ")+1
                try:
                    e = l.index(" upgrade")
                except:
                    e=l.index(" push")

                if s>e or s==-1:
                    continue

                key=l[s:e].strip()
                if key in activities.keys():
                    activities[key] = activities[key]+1
                else:
                    activities[key]=1
        else:
            continue

    with open(outFile, 'w', newline='\n') as csvfile:
        activity_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        activity_writer.writerow(["Sorted by Player"])
        activity_writer.writerow(["Player","Upgrade/Trophy pushing events"])
        keys=sorted(list(activities.keys()))
        for k in keys:
            activity_writer.writerow([k,activities[k]])

        value_sort=dict(sorted(activities.items(), key=lambda item: item[1], reverse=True))
        activity_writer.writerow(["\n"])
        activity_writer.writerow(["Sorted by Stats"])
        activity_writer.writerow(["Player", "Upgrade/Trophy pushing events"])
        for k, v in value_sort.items():
            activity_writer.writerow([k, v])

if __name__ == "__main__":
    #extract_activity_sikekick(sys.argv[1], sys.argv[2])

    #monthly
    extract_activity_sikekick("/home/zz/Work/cocanalyzer/input/July2021/ds-clan.csv",
                                "/home/zz/Work/cocanalyzer/input/July2021/ds-clan-summary.csv")

    '''
    /home/zz/Work/cocanalyzer/input/Apr2021/ds-clan.csv
    
    '''