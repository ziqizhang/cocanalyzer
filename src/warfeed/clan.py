import csv
import util
from warfeed import player as ply


class Clan:
    # name: clan name, as collected from sidekick discord war feed
    #
    def __init__(self, name: str):
        self._name = name
        self._players = []

        self._clan_total_attacks=0
        self._clan_total_stars=0
        self._clan_total_unused_attacks = 0
        self._clan_thlvl_attacks={}
        self._clan_thlvl_attackstars={}

        self._data_populated=False


    def summarize_attacks(self, outfolder=None):
        for p in self._players:
            if not p._data_populated:
                p.summarize_attacks()
            self.output_player_war_data(outfolder, p)

            self._clan_total_unused_attacks+=p._unused_attacks
            self._clan_total_attacks+=p._total_attacks
            self._clan_total_stars += p._total_stars

            for k, v in p._thlvl_attacks.items():
                c_thlvl_attacks = v
                if k in self._clan_thlvl_attacks.keys():
                    c_thlvl_attacks += self._clan_thlvl_attacks[k]
                self._clan_thlvl_attacks[k] = c_thlvl_attacks

            for k, data in p._thlvl_stars.items():
                if k in self._clan_thlvl_attackstars.keys():
                    clan_data = self._clan_thlvl_attackstars[k]
                else:
                    clan_data = {}

                for star, freq in data.items():
                    if star in clan_data.keys():
                        clan_data[star] += freq
                    else:
                        clan_data[star] = freq

                self._clan_thlvl_attackstars[k] = clan_data

        self._data_populated=True


    def output_player_war_data(self, out_folder, player:ply.Player):
        if out_folder is None:
            pass

        outFile = out_folder + "/" + util.normalise_name(player._name) + ".csv"

        with open(outFile, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["Total Stars Won", player._total_stars])
            writer.writerow(["Total Unused Attacks", player._unused_attacks])
            writer.writerow(["\n"])
            writer.writerow(["Target town hall level", "Stars", "Frequency"])

            ths = sorted(player._thlvl_attacks.keys())
            total_attacks = 0
            for th in ths:
                stars_and_freq = player._thlvl_stars[th]
                stars = sorted(stars_and_freq.keys())

                for s in stars:
                    total_attacks += stars_and_freq[s]
                    writer.writerow([th, s, stars_and_freq[s]])
            writer.writerow(["TOTAL", player._total_stars, total_attacks])

    def output_clan_war_data(self, out_csv: str):
        if not self._data_populated:
            self.summarize_attacks(out_csv)

        master_csv=out_csv+"/clan.csv"

        #player overview
        with open(master_csv, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["Player Overview"])
            writer.writerow(["Player","Total attacks","Unused attacks","Total stars", "Avg star per attack"])
            for p in self._players:
                if p._total_attacks==0:
                    avg=0
                else:
                    avg=round(p._total_stars/p._total_attacks,1)
                writer.writerow([p._name, p._total_attacks, p._unused_attacks, p._total_stars,
                                 avg])
            writer.writerow(["\n"])

        #clan overview
            writer.writerow(["Clan Overview"])
            writer.writerow(["Total attacks",self._clan_total_attacks])
            writer.writerow(["Total unused attacks", self._clan_total_unused_attacks])
            writer.writerow(["Total stars", self._clan_total_stars])
            writer.writerow(["\n"])
            writer.writerow(["Target town hall","3 stars","2 stars","1 star","0 star","Total attacks"])

            for thlvl in sorted(self._clan_thlvl_attacks.keys()):
                total_attacks = self._clan_thlvl_attacks[thlvl]
                star_freq = self._clan_thlvl_attackstars[thlvl]

                star3 = 0
                star2 = 0
                star1 = 0
                star0 = 0

                if 3 in star_freq.keys():
                    star3=star_freq[3]
                if 2 in star_freq.keys():
                    star2=star_freq[2]
                if 1 in star_freq.keys():
                    star1=star_freq[1]
                if 0 in star_freq.keys():
                    star0=star_freq[0]

                row=[thlvl, star3,star2,star1,star0, total_attacks]
                writer.writerow(row)
