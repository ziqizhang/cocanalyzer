
class Player:
    #name: player name, as collected from sidekick discord war feed
    #
    def __init__(self,name:str):
        self._name=name
        self._unused_attacks=0 # num of attacks this player had
        self._attacks=[] #attacks used and associated data
        self._defences=[] #num of times this player is attacked

        self._total_stars=0
        self._total_attacks=0
        self._thlvl_attacks={}
        self._thlvl_stars={}

        self._data_populated=False

    def summarize_attacks(self):
        #thlvl_attacks = {}
        #thlvl_stars = {} #key=0/1/2/3 stars; value=frequency

        for atk in self._attacks:
            if not atk._is_out:
                continue
            self._total_stars += atk._stars
            self._total_attacks+=1

            n = 1
            if atk._target_thlvl in self._thlvl_attacks.keys():
                n += self._thlvl_attacks[atk._target_thlvl]
            self._thlvl_attacks[atk._target_thlvl] = n

            s = atk._stars
            if atk._target_thlvl in self._thlvl_stars.keys():
                star_freq=self._thlvl_stars[atk._target_thlvl]
            else:
                star_freq={}
            self.update_stats(star_freq,s)
            self._thlvl_stars[atk._target_thlvl]=star_freq


        #return total_stars, thlvl_attacks, thlvl_stars
        self._data_populated=True

    def update_stats(self, star_freq:dict, stars:int):
        n=1
        if stars in star_freq.keys():
            n+=star_freq[stars]
        star_freq[stars]=n


    #TODO: test this
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

