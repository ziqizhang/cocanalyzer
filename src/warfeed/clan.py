
class Clan:
    # name: clan name, as collected from sidekick discord war feed
    #
    def __init__(self, name: str):
        self._name = name
        self._players=[]
        self._total_attacks=0
        self._attack_stars={} #key=target th lvl; value=stars


    def summarize_attacks(self):
        clan_total_stars=0
        clan_thlvl_attacks={}
        clan_thlvl_attackstars={}

        for p in self._players:

            p_totalstars, p_thlvl_attacks, p_thlvl_attackstars=p.summarize_attacks()

            clan_total_stars+=p_totalstars

            for k, v in p_thlvl_attacks.items():
                c_thlvl_attacks = v
                if k in clan_thlvl_attacks.keys():
                    c_thlvl_attacks+=clan_thlvl_attacks[k]
                clan_thlvl_attacks[k]=c_thlvl_attacks

            for k, data in p_thlvl_attackstars.items():
                if k in clan_thlvl_attackstars.keys():
                    clan_data = clan_thlvl_attackstars[k]
                else:
                    clan_data={}

                for star, freq in data.items():
                    if star in clan_data.keys():
                        clan_data[star]+=freq
                    else:
                        clan_data[star]=freq

                clan_thlvl_attackstars[k]=clan_data

        return clan_total_stars, clan_thlvl_attacks, clan_thlvl_attackstars


    def output_clan_war_data(self, out_csv:str):
        c_totalstars, c_thlvl_attacks, c_thlvl_attackstars=self.summarize_attacks()
        #todo continue here