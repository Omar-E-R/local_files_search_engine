# local_files_search_engine

Voici deux exemple de recherche:

<img src="Screenshot from 2021-12-16 17-50-27.png" alt="Screenshot from 2021-12-16 17-50-27" style="zoom:50%;" />

<img src="Screenshot from 2021-12-16 17-50-36.png" alt="Screenshot from 2021-12-16 17-50-36" style="zoom:80%;" />



## Stop-Words (mots vides)

Ce projet utilise les mots vides fournis par la librairie **Spacy** de python.

```python
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stopwords_list
```

## Base de données

La base de données utilisées est **Postgresql**.

<img src="Screenshot from 2021-12-16 18-19-15.png" alt="Screenshot from 2021-12-16 18-19-15" style="zoom:50%;" />

## Back-end

Django est le backend. un repertoire nommé google_api contient le back-end qui est un api.

### Indexing

Dans le fichier `app.py`, il existe le script python d'indexation. Au lancement du serveur  avec `python3 manage.py runsurver`, le serveur lance le script qui cherche dans le repertoire `text_files` les fichiers txt *(qui sont énorme jusqu'à 1300 lignes de texte)* et indexe tous les fichiers qui ne sont pas indexés et se trouvant dans la base données. *(On ne refait pas le travail au démarrage mais on check si il y a de nouveau fichier non indexés)*. L'indexation est très rapide et se fait en utilisant les fonctions de la librairie `pandas` de python. C'est la solution la plus rapide parmis les autres projet en classe.

Pour faire une requete de recherche en API REST get:

```
http://localhost:8000/google/index/?search=MOTS
```

Les resultats seront envoyé au format JSON en utilisant une fonctionnalité de Django qui est très optimisé et rapide/

## Front-end

React-JS est le front avec une fonctionnalité de "hook-rebound" et de "active-search". Dès l'écriture dans la barre de recherche on peut avoir de résultat. Donc on n'aura ni à rafraichir la page ni à clicker sur entrer à chaque recherche.

## Script de mise à jour

J'ai crée un script `start_server.sh`  qui relance le serveur quand il y a un nouveau fichier ajouter pour qu'il soit indexer.



J'ai fait ce projet en un seul jour.
