
# Fantoir-groupe3

![logo](screenshots/brief_logo.png)

La société DVD Subject Blue souhaite développer une intelligence artificielle pour son prochain jeu : L'ombre de Morbac. Le principe est de gagner contre Morbac, expert au jeu du Morpion. Pour que son jeu rencontre le succès, il faut que l'intelligence artificielle soit à la hauteur. Et c'est pour cela que la société vous sollicite !


### Pré-requis

* Python 3
* Installer les librairies dans [requirement.txt](https://github.com/moh-IA/Morpion/blob/develop/msi/requirement.txt "requirement.txt")
* Installer pygame via **pip** : *pip install pygame*


### Fonctionnalités

**4 types de joueurs ont été implémentés:**

* Joueur Humain : à vous de jouer!
* Bot Random : parfois faire n'importe quoi ça fonctionne ... mais n'espérez pas trop de challenge...
* Bot réseau de neurone : une vrais IA qui vous donnera des sueurs froides. Par contre elle est entrainée via un bot random ce qui limite ses compétences.
* Bot Min/Max : l'IA que vous ne pourrez jamais battre!


### Utilisation

**2 modes d'affichage** 

* Mode console: disponible en lancant [console_launcher.py](https://github.com/moh-IA/Morpion/blob/develop/msi/console_launcher.py "console_launcher.py")

![console](https://github.com/moh-IA/Morpion/blob/develop/msi/screenshots/console_screen.png)


* Mode graphique: disponible en lancant [pygame_launcher.py](https://github.com/moh-IA/Morpion/blob/develop/msi/pygame_launcher.py "pygame_launcher.py")
*en mode graphique, profitez du son pour une meilleur expérience*

![graphic](https://github.com/moh-IA/Morpion/blob/develop/msi/screenshots/graphic_screen.gif)

### Fonctionnement
* Le modèle CNN entrainé à partir de 2 bots random. Il agit un peu comme quelqu'un ayant eu comme partenaire un mauvais entraineur. Selon les simulations, sa performance est plus au moins bonne mais celle fournit dans Github est plutôt efficace. Il n'est pas nécessaire de rejouer des simulations à chaque fois, le modèle est sauvegardé dans [models/cnn.model](https://github.com/moh-IA/Morpion/blob/develop/msi/models/cnn.model "cnn.model")

* Le modèle Min/max privilégie le meilleur coup à la profondeur la moindre, ainsi il est quasiment imbattable! Afin de gagner du temps de calcul, chaque coup calculé est stocké dans le fichier [models/minmax.saves](https://github.com/moh-IA/Morpion/blob/develop/msi/models/minmax.saves "minmax.saves") : puisque l'algorithme offrira toujours la même réponse au même tableau, il n'est pas nécessaire de relancer le calcul à chaque fois. Il est possible de supprimer ce fichier afin de forcer le recalcule (mais celà ne changera rien aux réponses de l'IA)

### Méa-culpa
* Le modèle CNN est issue de https://medium.com/swlh/tic-tac-toe-and-deep-neural-networks-ea600bc53f51 et n'a pas été optimisé comme il le devrait


