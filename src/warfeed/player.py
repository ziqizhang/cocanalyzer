
class Player:
    #name: player name, as collected from sidekick discord war feed
    #
    def __init__(self,name:str):
        self._name=name
        self._attacks_available=0 # num of attacks this player had
        self._attacks=[] #attacks used and associated data
        self._defences=[] #num of times this player is attacked

    def summarize_attacks(self):
        thlvl_attacks = {}
        thlvl_stars = {} #key=0/1/2/3 stars; value=frequency

        total_stars=0
        for atk in self._attacks:
            if not atk._is_out:
                continue
            total_stars += atk._stars

            n = 1
            if atk._target_thlvl in thlvl_attacks.keys():
                n += thlvl_attacks[atk._target_thlvl]
            thlvl_attacks[atk._target_thlvl] = n

            s = atk._stars
            if atk._target_thlvl in thlvl_stars.keys():
                star_freq=thlvl_stars[atk._target_thlvl]
            else:
                star_freq={}
            self.update_stats(star_freq,s)
            thlvl_stars[atk._target_thlvl]=star_freq

        return total_stars, thlvl_attacks, thlvl_stars

    def update_stats(self, star_freq:dict, stars:int):
        n=1
        if stars in star_freq.keys():
            n+=star_freq[stars]
        star_freq[stars]=n


    def average_atk_stars(self):

        if len(self._attacks)==0:
            return 0, dict()
        total, thlvl_attacks, thlvl_stars = self.summarize_attacks()

        avg_star={}
        for k in thlvl_attacks.keys():
            n = thlvl_attacks[k]
            s = thlvl_stars[k]
            avg_star[k] = round(n/s,1)
        return round(total/len(self._attacks),1), avg_star

