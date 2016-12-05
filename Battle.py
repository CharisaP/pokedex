from random import randint
class Pokemon:
    def __init__(self,name,typ,lvl):
        self.name = name
        self.typ = typ
        self.lvl = lvl
        self.Strength = lvl 
        self.Defense = lvl
        self.HP = 100

    def calc_damage(self,opponent):
        damage = randint(0, 5) + self.Strength - opponent.Defense
        if damage <= 0:
            return "{} evades {}'s attack!".format(opponent.name, self.name)
        else:
            opponent.HP = opponent.HP - damage
            return "{} attacks {} for {} points of damage!".format(self.name, opponent.name, str(damage))
    def calc_SnD(self,opponent):
        x = dict()
        Matrix = [[0,1,2,1,0,0,1],[2,0,1,2,0,0,0],[1,2,0,0,0,0,0],
                [2,1,0,0,0,2,1],[0,0,0,0,0,0,0],[2,0,0,1,0,0,2],
                [2,0,0,2,0,1,0]]
        x['Grass'] = 0
        x['Fire'] = 1
        x['Water'] = 2
        x['Bug'] = 3
        x['Normal'] = 4
        x['Psychic'] = 5
        x['Poison'] = 6
        i = x[self.typ]
        j = x[opponent.typ]
        if Matrix[i][j] == 1:
            self.Strength += 10
            self.Defense *= 5
            opponent.Strength += 15
            opponent.Defense += 10
        elif Matrix[i][j] == 2:
            self.Strength += 15
            self.Defense += 10
            opponent.Strength += 10
            opponent.Defense += 5
    
def PokemonBattle(OwnedMon,WildMon):

    Txt = []
    OwnedMon.calc_SnD(WildMon)
    winner = None
    while True:
        Txt.append(OwnedMon.calc_damage(WildMon))
        if OwnedMon.HP < 1:
            winner = WildMon.name
            Txt.append("Your {} Lost.".format(OwnedMon.name))
            break
        elif WildMon.HP < 1:
            winner = OwnedMon.name
            Txt.append("Your {} Won!".format(OwnedMon.name))
            break
        Txt.append(WildMon.calc_damage(OwnedMon))
    return Txt,winner 