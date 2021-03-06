
class Attack:
    #id = an arbitrary id
    #target_thlvl= town hall level of the target being attacked
    #target_thlvl= town hall level of the attacker
    #stars = #of stars won
    #is_outgoing: True indicating an attack; False indicating a defence.
    def __init__(self,id:str, target_thlvl:int, source_thlvl:int, stars:int, is_outgoing:bool):
        self._id=id
        self._target_thlvl=target_thlvl
        self._source_thlvl=source_thlvl
        self._stars=stars
        self._is_out = is_outgoing
