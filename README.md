# doctolib-bot

Cherche sur Doctolib les rendez-vous disponibles pour les +18 ans sans comorbidités dans les 24 heures à venir.
Nécessite python 3, et pip.

## Installation
```bash
pip install -r requirements.txt
```

## Utilisation
Exemple:
```bash
python doctolib.py --location lyon --max-page 3
```
```bash
python doctolib.py --location pornichet --max-page 5 --forever --interval 10
```

Toutles les options:
  --location TEXT           La ville autour de laquelle rechercher
  --max-page INTEGER        Nombre de page à scanner sur Doctolib
  --quiet / --no-quiet      Désactive le logging. Défaut : Faux
  --forever / --no-forever  Si le programme doit s'executer indéfiniment ou
                            chercher une seule fois. Défaut : Vrai


  --interval INTEGER        Intervalle en minutes entre chaque
                            rafraichissements si --forever est utilisé.
                            Attention de ne pas mettre trop court, on ne sait
                            pas si doctolib fait des bans. Défaut : 5.

  --notify / --no-notify    Si le programme doit afficher une notification si
                            un créneau est trouvé. Défaut : Vrai

  --help                    Pour retrouver cette documentation
