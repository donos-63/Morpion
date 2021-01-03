from player import Player

class Human(Player):

    def play(self, game):
        
        ligne = self.__input_coordonnee('ligne: ')
        col = self.__input_coordonnee('colonne: ')
        return (x-1, y-1)

    def __input_coordonnee(text):
        accepted = False
        while not accepted:
            coord = input(text)
            try:
                coord = int(coord)
                accepted = True
            except:
                pass
        return coord - 1

if __name__ == '__main__':
    h1 = Human('1')
    h2 = Human('1')
    
    print(h1 == h1)
    print(h1 == h2)
    