class Pers():
    '''изучаем классы. допустим у персонажа есть количество жизней и брони, вводим силу наносимого удара
    и программа выводит выжил ли он или нет'''
    health = 200
    steel = 50

    def __init__(self, damage=900):
        self.damage = damage
        '''если показатели брони меньше силы удара, то вычитаем из показателей жизней разницу силы удара и брони'''
        if self.steel < int(self.damage):
            self.health = self.health - int(self.damage) + self.steel

    def dead(self):
        if self.health > 0:
            return "еще жив"
        else:
            return "погиб"


hit = input("Сила удара - ")
'''определяем переменную test классом Pers'''
test = Pers(hit)
print(test.dead())
