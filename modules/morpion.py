from typing import Tuple

from modules.plateau import Plateau

class Morpion:
    """
    Gere le jeu du morpion
    """
    
    def __init__(self) -> None:
        self._joueur1 = "X"
        self._joueur2 = "O"
        self._plateau = Plateau()

    def jouer(self) -> None:
        """
        Permet de lancer le jeu
        """
        
        print("Bienvenue sur le jeu du morpion.")
        print("Etes-vous prêt à affronter Morbac ?")
        
        while not self.est_termine():
            self.jouer_tour(self._joueur1)
            self.jouer_tour(self._joueur2)


    def jouer_tour(self, player: str) -> None:
        """
        Faite un tour de Morpion (les deux joueurs placent leur jeton)
        """

        print("Au tour du joueur avec le pion {}".format(player))

        resultat_tour = False

        while not resultat_tour:
            position_x_joueur: str = input("Ou voulez-vous jouer en X ?")
            position_x_parse = Morpion.verifier_et_cast_caractere(position_x_joueur)

            position_y_joueur: str = input("OU voulez-vous jouer en Y ?")
            position_y_parse = Morpion.verifier_et_cast_caractere(position_y_joueur)

            if position_x_parse == -1 or position_y_parse == -1:
                print("Vous devez rentrer un nombre entre 1 et 3")
                resultat_tour = False
                continue

            position_tableau: Tuple[int, int] = (position_x_parse, position_y_parse)
            resultat_tour = self._plateau.jouer_jeton(player, position_tableau)

            if not resultat_tour:
                print("Un jeton existe déjà à cet endroit, merci d'en choisir un autre")

    def verifier_et_cast_caractere(position_a_verifier: str) -> int:
        """
        Valide que l'entrée est utilisateur est conforme. Renvoi le chiffre auquel on a soustrait 1 pour connaitre la position dans le tableau (index 0) 
        ou -1 si l'entrée utilisateur n'est pas valide (ex: lettre).
        """
        try:
            return int(position_a_verifier) - 1
        except ValueError:
            return -1

    def est_termine(self) -> bool:
        """
        Vérifie si un joueur à gagner
        """
        rows = self._plateau.get_rows()

        for ligne_a_valider in rows:

            cellule_temoin = ligne_a_valider[0]

            if cellule_temoin == None:
                continue

            ligne_validation = [cellule_temoin, cellule_temoin, cellule_temoin]

            if ligne_a_valider == ligne_validation:
                return True

        return False
