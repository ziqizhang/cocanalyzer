
from warfeed import attack as atk
from warfeed import player as ply
from warfeed import clan as cln
import util
import pandas as pd
import re, sys

OPPONENT_ATTACK_STAR="starD"
CLAN_ATTACK_STAR="sk_star_new"
NO_STAR="sk_star_empty"
ATTACK="sk_arrow_right"
DEFENCE="sk_arrow_left"


def find_remainig_attacks(text_remaining):
    # assuming syntax like "**1 Remaining Attack**"
    last_line = text_remaining.split("\n")[-1]
    remaining = int(last_line[2:])
    return remaining

def update_remaining_attacks(text, player_mapping, remaining_attacks):
    lines = text.split("\n")
    for rowidx in range(1, len(lines)):
        row = lines[rowidx]
        if (row.startswith(":b")):
            startindex = row.rindex(":")
            player_name = util.normalise_name(row[startindex + 1:])
            if player_name in player_mapping.keys():
                player = player_mapping[player_name]
                player._unused_attacks += remaining_attacks
            else:
                player = ply.Player(player_name)
                player_mapping[player_name] = player
        elif (row.startswith("**")):
            break

def parse_sidekick_warfeed(inFile, clanname):
    data = pd.read_csv(inFile, header=0, delimiter=',', quoting=0, encoding="utf-8",
                       ).fillna("none")
    data = data.values


    player_mapping={}

    attack_id=1
    for r in data:
        print(r[2])
        #check if the message is from sidekick
        if 'sidekick' not in r[1].lower():
            continue

        #check if the message is a message about attack.
        if r[3].startswith(":star") or r[3].startswith(":sk_star"):
            lines=r[3].split("\n")

            #parse each line
            #e.g.: :sk_star_new::sk_star_new::sk_star_new: :s100::per: :b35: CerMaC :t9: :sk_arrow_right: :t8: :b33:
            #:starD::starD::sk_star_empty: :99::per: :b36: xanderthegreat :t9: :sk_arrow_left: :t9: :b31:
            #:starD::starD::starD: :s100::per: :b6: BlackStallion97 :t11: :sk_arrow_left: :t13: :b1:
            for l in lines:
                ol=l #debug use only
                l=re.sub(r'(:+\s*:*)', ':', ol)
                parts = l.split(":")

                if len(parts)!=13:
                    print("\t error on line: "+ol)
                    continue

                stars=0
                for i in range(1,4):
                    if parts[i].strip()!=NO_STAR:
                        stars+=1

                outgoing=True
                if parts[9]==DEFENCE:
                    outgoing=False

                source_thlvl=parts[8].strip()
                target_thlvl=parts[10].strip()
                player_name=util.normalise_name(parts[7])

                if player_name=="Z.Z":
                    print("")

                if player_name in player_mapping.keys():
                    player=player_mapping[player_name]
                else:
                    player = ply.Player(player_name)

                attack=atk.Attack(str(attack_id),target_thlvl,
                                  source_thlvl,stars, outgoing)
                if outgoing:
                    player._attacks.append(attack)
                else:
                    player._defences.append(attack)

                player_mapping[player_name] = player
                attack_id+=1


        if "remaining attack" in r[3].lower():#to check remaining attacks
            try:
                sidx= r[3].lower().index("2 remaining attack")
                remaining_attacks = 2

                text=r[3][sidx:]
                update_remaining_attacks(text, player_mapping, remaining_attacks)
            except:
                pass

            try:
                sidx = r[3].lower().index("1 remaining attack")
                remaining_attacks = 1

                text = r[3][sidx:]
                update_remaining_attacks(text, player_mapping, remaining_attacks)
            except:
                pass


    clan = cln.Clan(clanname)
    clan._players=list(player_mapping.values())
    return clan

if __name__ == "__main__":
    clan_war_data=parse_sidekick_warfeed(sys.argv[1],sys.argv[2])

    #this will output player data to a folder
    clan_war_data.summarize_attacks(outfolder=sys.argv[3])

    clan_war_data.output_clan_war_data(sys.argv[3])

    #weekly:
    '''
    /home/zz/Work/cocanalyzer/input/weekly/war-log.csv
    DeadSages
    /home/zz/Work/cocanalyzer/input/weekly/tmp
    '''

    #monthly:
    '''
    /home/zz/Work/cocanalyzer/input/Mar2021/war-feed.csv
    DeadSages
    /home/zz/Work/cocanalyzer/input/Mar2021/players
    '''

    '''
    /home/zz/Work/cocanalyzer/input/Apr2021/ds-war.csv
    DeadSages
    /home/zz/Work/cocanalyzer/input/Apr2021/dswar
    '''

    '''
        /home/zz/Work/cocanalyzer/input/Apr2021/dse-war.csv
        DeadSagesElite
        /home/zz/Work/cocanalyzer/input/Apr2021/dsewar
        '''