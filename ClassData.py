class Player:
    def __init__(self, match_individual_id, account_id, mmr, behaviour_score, last_20_match_wr, wr, hero_id, hero_name, abilities, hero_facet, hero_innate, potential_shard_ability, potential_scepter_ability):
        self.match_individual_id = match_individual_id
        self.account_id = account_id
        self.mmr = mmr
        self.behaviour_score = behaviour_score
        self.last_20_match_wr = last_20_match_wr
        self.wr = wr
        self.hero_id = hero_id
        self.hero_name = hero_name
        self.abilities = abilities
        self.hero_facet = hero_facet
        self.hero_innate = hero_innate
        self.potential_shard_ability = potential_shard_ability
        self.potential_scepter_ability = potential_scepter_ability

class Match:
    def __init__(self, match_id, dire_Player, radiant_Player):
        self.match_id = match_id
        self.dire_Player = dire_Player
        self.radiant_PLayer = radiant_Player
        






