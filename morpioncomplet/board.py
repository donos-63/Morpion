class Board:

    def __init__(self, size = 3, verbose = True):
        self.size = size
        self.verbose = verbose
        self.table = [[False for x in range(self.size)] for y in range(self.size)]

    def show(self):
        if self.verbose is False:
            return

        for line in self.table:
            for col in line:
                
                if col is False:
                    val = "." 
                else:
                    val = str(col)

                print(" "+ val, end="")
            print()

    def full(self):
        for ligne in self.table:
            if False in ligne:
                return False
        return True

    def __is_same_values(ma_liste):
        mon_set = set(ma_liste)
        if list(mon_set)[0] is not False and len(mon_set) == 1:
            return True
        return False

    def ligne(self):
        for ligne in self.table:
            if Board.__is_same_values(ligne):
                return True
        return False

    def col(self):
        for ligne in range(self.size):
            colonne = []

            for col in range(self.size):
                colonne.append(self.table[col][ligne])

            if Board.__is_same_values(colonne):
                return True

        return False
    
    def diagonale(self):
        # j'ai pas d'idee
        d1 = [ self.table[0][0], self.table[1][1], self.table[2][2] ] # +1 +1
        d2 = [ self.table[0][2], self.table[1][1], self.table[2][0] ] # +1 -1
        for d in [d1, d2]:
            if Board.__is_same_values(d):
                return True
        return False

    def is_valid_action(self, ligne, col):
        if self.table[ligne][col] is False:
            return True
        else:
            return False

    def placer(self, ligne, col, caractere):
        if ligne not in range(self.size) or col not in range(self.size):
            if self.verbose: print("Out of board !")
            return False

        if self.table[ligne][col] is not False:
            if self.verbose: print(f"Emplacement occupe au coordonnees {ligne} et {col} !\nPar le signe ", self.table[ligne][col])
            return False
        
        self.table[ligne][col] = caractere
        return True
