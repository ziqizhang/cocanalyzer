
'''
this file parses sidekick end of week digest and work out clan total for gold loot etc.

you need
- an input of the previous week
- an input of the current week

as data are accumulative, so need to work out the difference
'''

import locale, sys

def parse_data(in_file):
    data = {}

    f = open(in_file, encoding='utf-8', errors='ignore')
    lines=f.readlines()

    curr=None
    total=0
    for l in lines:
        l=l.strip()
        if "looted" in l.lower() or "donations" in l.lower() or "attack" in l.lower() \
                or "trophies" in l.lower() or "clan game" in l.lower():
            label = l
            if ":" in label:
                label = label[label.rindex(":")+1:].strip()
            if curr is None:
                curr=label
                continue
            elif curr!=label:
                data[curr] = total
                curr=label
                total = 0
                continue
        else:
            parts=l.split(" ", 1)
            try:
                num = int(parts[0].replace(',', ''))
                total+=num
            except:
                continue
    if curr is not None:
        data[curr]=total
    return data

def calculate_week_difference(in_this_week,in_prev_week):
    prev = parse_data(in_prev_week)
    this = parse_data(in_this_week)

    diffs={}
    for k,v in this.items():
        if k in prev.keys():
            prevv = prev[k]
        else:
            prevv=0
        dif = v - prevv
        diffs[k]=dif

    print(diffs)

if __name__ == "__main__":
    calculate_week_difference(sys.argv[1],sys.argv[2])

