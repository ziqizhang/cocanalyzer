
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


def parse_sidekick_warfeed(inFile, clanname):
    data = pd.read_csv(inFile, header=0, delimiter=',', quoting=0, encoding="utf-8",
                       ).fillna("none")
    data = data.values


    player_mapping={}

    attack_id=1
    for r in data:
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
            sidx= r[3].lower().index("remaining attack")
            text_remaining = r[3][0:sidx].strip()
            remaining_attacks = find_remainig_attacks(text_remaining)

            text=r[3][sidx:]

            lines=text.split("\n")
            for rowidx in range(1,len(lines)):
                row = lines[rowidx]
                if (row.startswith(":b")):
                    startindex=row.rindex(":")
                    player_name = util.normalise_name(row[startindex+1:])
                    if player_name in player_mapping.keys():
                        player = player_mapping[player_name]
                        player._unused_attacks+=remaining_attacks
                    else:
                        player = ply.Player(player_name)
                        player_mapping[player_name]=player

    clan = cln.Clan(clanname)
    clan._players=list(player_mapping.values())
    return clan

if __name__ == "__main__":
    clan_war_data=parse_sidekick_warfeed(sys.argv[1],sys.argv[2])
    clan_war_data.summarize_attacks(outfolder=sys.argv[3])