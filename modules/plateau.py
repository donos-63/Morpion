from typing import List, Tuple


class Plateau:
    """
    Represente le plateau de jeu
    """
    
    def __init__(self) -> None:
        self._tableau: List[List[str]] = [[None, None, None],[None, None, None],[None, None, None]] # Ou en boucle for

    def jouer_jeton(self, player: str, position: Tuple[int, int]) -> bool:
        """
        Place un jeton sur le plateau
        """

        if(position[0] < 0 or position[0] >= 3):
            return False

        jeton_existant = self._tableau[position[0]][position[1]]

        if(jeton_existant == None):
            self._tableau[position[0]][position[1]] = player

            return True
        else:
            return False

    def get_rows(self) -> List[List[str]]:
        """
        On récupères la liste de toutes les lignes à valider
        """
        rows: List[List[str]] = []

        for index in range(3):
            # Récupère toutes les lignes
            rows.append(self._tableau[index])

            # TODO : Colonnes et diagonales

        return rows   