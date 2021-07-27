'''
This processes two files.

1. the data exported from sidekick for stars etc, by:
/export for:CurrentChanel number:2

2. the discord messages exported by the discordexporter, for getting missed attacks


'''


from warfeed import attack as atk
from warfeed import player as ply
from warfeed import clan as cln
import util
import pandas as pd
import re, sys, datetime


def find_remainig_attacks(text_remaining):
    # assuming syntax like "**1 Remaining Attack**"
    last_line = text_remaining.split("\n")[-1]
    remaining = int(last_line[2:])
    return remaining

def update_remaining_attacks(text, player_mapping, remaining_attacks):
    lines = text.split("\n")
    for rowidx in range(1, len(lines)):
        row = lines[rowidx]
        if (row.startswith(":b") or row.startswith(":s:")):
            startindex = row.rindex(":")
            player_name = util.normalise_name(row[startindex + 1:])
            if player_name in player_mapping.keys():
                player_mapping[player_name]+=remaining_attacks
            else:
                player_mapping[player_name] = remaining_attacks
        elif (row.startswith("**")):
            break

def parse_sidekick_missed_attacks(inFile):
    data = pd.read_csv(inFile, header=0, delimiter=',', quoting=0, encoding="utf-8",
                       ).fillna("none")
    data = data.values


    player_unused={}

    for r in data:
        print(r[2])
        #check if the message is from sidekick
        if 'sidekick' not in r[1].lower():
            continue


        if "remaining attack" in r[3].lower():#to check remaining attacks
            try:
                sidx= r[3].lower().index("2 remaining attack")
                remaining_attacks = 2

                text=r[3][sidx:]
                update_remaining_attacks(text, player_unused, remaining_attacks)
            except:
                pass

            try:
                sidx = r[3].lower().index("1 remaining attack")
                remaining_attacks = 1

                text = r[3][sidx:]
                update_remaining_attacks(text, player_unused, remaining_attacks)
            except:
                pass


    return player_unused


def parse_sidekick_export_wardata(inFile, clanname, missed_attacks:dict, start_date_str,
                                  col_attacker="name", col_stars="stars",
                                  col_defenderth="defenderTH",
                                  col_attackerth="thLevel",
                                  col_ishomeclan="attacker_is_home_clan",
                                  col_wartime="war_start_time",
                                  col_defender="defenderName"
                                  ):
    player_mapping = {}
    date_time_obj = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')


    data = pd.read_csv(inFile, header=0, delimiter=',', quoting=0, encoding="utf-8",
                       ).fillna("none")

    attack_id=0
    for index, row in data.iterrows():
        ishomeclan = row[col_ishomeclan]
        if ishomeclan!=1:
            continue #for now ignore defence

        time=datetime.datetime.strptime(row[col_wartime], '%Y-%m-%d %H:%M:%S')
        if time < date_time_obj:
            continue

        attack_id+=1
        player_name = row[col_attacker]
        player_th = row[col_attackerth]
        defenderth = row[col_defenderth]

        player_name = util.normalise_name(player_name)

        stars=row[col_stars]


        if player_name in player_mapping.keys():
            player = player_mapping[player_name]
        else:
            player = ply.Player(player_name)

        attack = atk.Attack(str(attack_id), defenderth,
                            player_th, stars, True)
        player._attacks.append(attack)


        player_mapping[player_name] = player
        attack_id += 1

    for k, v in missed_attacks.items():
        if k in player_mapping.keys():
            player = player_mapping[k]
            player._unused_attacks=v
        else:
            player = ply.Player(k)
            player._unused_attacks=v
            player_mapping[k]=player

    clan = cln.Clan(clanname)
    clan._players = list(player_mapping.values())
    return clan


if __name__ == "__main__":
    '''
/home/zz/Work/cocanalyzer/input/Apr2021/ds-war.csv
/home/zz/Work/cocanalyzer/input/Apr2021/DeadSages_war_attacks.csv
deadsages
2021-04-09
/home/zz/Work/cocanalyzer/input/Apr2021/dswar
        '''

    '''
/home/zz/Work/cocanalyzer/input/Apr2021/dse-war.csv
/home/zz/Work/cocanalyzer/input/Apr2021/DeadSages_Elite_war_attacks.csv
deadsageselite
2021-04-25
/home/zz/Work/cocanalyzer/input/Apr2021/dsewar
        '''


    #for missed attacks
    discord_war_export_file=sys.argv[1]
    #sidekick export war file
    sidekick_war_export=sys.argv[2]
    clan=sys.argv[3]
    start_date=sys.argv[4]
    out_folder=sys.argv[5]

    missed_attacks=parse_sidekick_missed_attacks(discord_war_export_file)

    #this will output player data to a folder
    clan_war_data = parse_sidekick_export_wardata(sidekick_war_export, clan, missed_attacks,start_date)

    # this will output player data to a folder
    clan_war_data.summarize_attacks(outfolder=out_folder)

    clan_war_data.output_clan_war_data(out_folder)


    #monthly:

    '''
    /home/zz/Work/cocanalyzer/input/June2021/ds-war.csv
    DeadSages
    /home/zz/Work/cocanalyzer/input/June2021/dswar
    '''
'''
    /home/zz/Work/cocanalyzer/input/June2021/dse-war.csv
/home/zz/Work/cocanalyzer/input/June2021/DeadSages_Elite_war_attacks.csv
deadsageselite
2021-05-24
/home/zz/Work/cocanalyzer/input/June2021/dsewar
        '''


'''
    /home/zz/Work/cocanalyzer/input/June2021/ds-war.csv
/home/zz/Work/cocanalyzer/input/June2021/DeadSages_war_attacks.csv
deadsages
2021-05-24
/home/zz/Work/cocanalyzer/input/June2021/dswar
'''