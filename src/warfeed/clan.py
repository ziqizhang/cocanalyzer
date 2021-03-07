import csv
import util


class Clan:
    # name: clan name, as collected from sidekick discord war feed
    #
    def __init__(self, name: str):
        self._name = name
        self._players = []
        self._total_attacks = 0
        self._attack_stars = {}  # key=target th lvl; value=stars

    def summarize_attacks(self, outfolder=None):
        clan_total_stars = 0
        clan_thlvl_attacks = {}
        clan_thlvl_attackstars = {}

        for p in self._players:

            p_totalstars, p_thlvl_attacks, p_thlvl_attackstars = p.summarize_attacks()
            self.output_player_war_data(outfolder, p._name, p_totalstars, p._unused_attacks,
                                        p_thlvl_attacks, p_thlvl_attackstars)

            clan_total_stars += p_totalstars

            for k, v in p_thlvl_attacks.items():
                c_thlvl_attacks = v
                if k in clan_thlvl_attacks.keys():
                    c_thlvl_attacks += clan_thlvl_attacks[k]
                clan_thlvl_attacks[k] = c_thlvl_attacks

            for k, data in p_thlvl_attackstars.items():
                if k in clan_thlvl_attackstars.keys():
                    clan_data = clan_thlvl_attackstars[k]
                else:
                    clan_data = {}

                for star, freq in data.items():
                    if star in clan_data.keys():
                        clan_data[star] += freq
                    else:
                        clan_data[star] = freq

                clan_thlvl_attackstars[k] = clan_data

        sum = 0
        for v in clan_thlvl_attacks.values():
            sum += v
        return clan_total_stars, clan_thlvl_attacks, clan_thlvl_attackstars

    def output_player_war_data(self, out_folder, player_name, p_totalstars,
                               p_total_unused,
                               p_thlvl_attacks, p_thlvl_attackstars):
        if out_folder is None:
            pass

        outFile = out_folder + "/" + util.normalise_name(player_name) + ".csv"
        with open(outFile, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(["Total Stars Won", p_totalstars])
            writer.writerow(["Total Unused Attacks", p_total_unused])
            writer.writerow(["\n"])
            writer.writerow(["Target town hall level", "Stars", "Frequency"])

            ths = sorted(p_thlvl_attacks.keys())
            total_attacks = 0
            for th in ths:
                stars_and_freq = p_thlvl_attackstars[th]
                stars = sorted(stars_and_freq.keys())

                for s in stars:
                    total_attacks += stars_and_freq[s]
                    writer.writerow([th, s, stars_and_freq[s]])
            writer.writerow(["TOTAL", p_totalstars, total_attacks])

    def output_clan_war_data(self, out_csv: str):
        c_totalstars, c_thlvl_attacks, c_thlvl_attackstars = self.summarize_attacks()
        # todo continue here
