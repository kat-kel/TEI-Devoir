# TEI-Devoir

[Consignes de l'évaluation : github.com/Segolene-Albouy](https://github.com/Segolene-Albouy/XML-TEI_M2TNAH/blob/main/ConsignesEvaluation.md)

    
# Ma Méthode de Nettoyer le Texte

## Compétences : RegEx, Python, et création d'une librairie python

1. Télécharger des images JPEG en haute résolution de Gallica qui extrait uniquement le contenu du feuilleton.
	* Travailler sur [chapitre XI](https://gallica.bnf.fr/ark:/12148/bpt6k4775593/f1.image) et [chapitre XII](https://gallica.bnf.fr/ark:/12148/bpt6k4775601/f1.image) de _Daniella_ par George Sand.

2. Transformer le JPEG en PDF. (Moi, j'ai utilisé le logiciel Tesseract)

3. Transcrire dans [eScriptorium](https://traces6.paris.inria.fr/) le fichier PDF, en notant dans un fichier à part des mots en italiques et des coquilles.

4. Sortir de l'eScriptorium des fichiers TEXT et les stocker dans le dossier du projet __data/out_eScriptorium__.
![exemple 1](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-03-47.png?raw=true)

5. Faire deux étapes de petites modifications à la main et sauvgarder les fichiers modifiés dans un nouveau dossier __data/in_transcription__.
![exemple 2](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-03-01.png?raw=true)

	* D'après les notes prises lors de la transcription dans eScriptorium :

		* Entourner des mots en italique par deux underscores
		* Suivre des coquilles avec \[sic]
		* Entourner par des crochets des corrections des lettres et/ou des mots illisibles, e emple --> e\[x]emple

	* Récupérer les paragraphes de l'imprimé :

		* Pour fusionner des mots divisés à la fin d'une ligne, sélectionner ```(-)\n``` et le remplacer avec rien.

		* Pour fusionner des phrases qui traversent des lignes, sélectionner ```(\b|[__]|\,|\;)\n``` et le remplacer avec ```$1 ```, avec un espace à la fin qui remplacera le saut de ligne.

		* Mais si le texte d'origine ne contient pas d'espaces pour diviser des paragraphes--comme celui qui sort de l'eScriptorium--cette méthode se trompera sur les phrases qui commencent une ligne mais pas un nouveau paragraphe. Il faut donc vérifier avec l'image transcrite que les lignes de texte représentent les paragraphes.

6. Combiner tous les fichiers de __data/in_transcription/__ dans un seul fichier en utilisant un programme que j'ai écrit, ```merge.py```. Grâce à la méthode @click, ```merge.py``` peut démarrer deux fonctions. La fonction ```add``` ajoute les contenus textuels d'un fichier dans le fichier principal : __data/in_transcription/full_text.txt__. Elle créera ce dernier fichier s'il n'existe pas déjà. La deuxième fonction, ```erase```, efface tous les contenus du fichier principal, qui est utile s'il y a un erreur d'utilisateur ou pour commencer un nouveau fichier composé.
![exemple 3](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-02-24.png?raw=true)

	* La fonction @click ```add``` exige deux arguments dans l'ordre suivant :
	
		1. Le nom du fichier sans l'extension .txt (le fichier doit se trouve dans __data/in_transcription/__)
		
		2. L'id xml de la source transcrite (l'id devrait être court et sans espaces)

		* Exemple : ```python merge.py add 19_janvier_1 19Jan```. Depuis le terminal, cette ligne démarrera la fonction ```add``` et ensuite récrira le fichier __data/in_transcription/19_janvier_1.txt__ vers __data/in_transcription/full_text.txt__ avec des modifications de l'XML. De plus, elle lui donnera l'id "19Jan" qui servira à l'encodage XML, parce que le deuxième argument entrée est la chaîne "19Jan."

		* S'il y a déjà des données récrites dans le fichier __data/in_transcription/full_text.txt__, la fonction ```add``` le reconnaîtra et ajoutera les nouvelles à la fin, en gardant \<body> en haut du document et <\\body> en bas. Par contre, la fonction compte sur l'utilisateur d'ajouter des fichiers dans leur propre ordre.

	* Dans le cas où s'effectue un erreur d'utilisateur, il est recommandé d'appeller la fonction ```erase``` du programme ```merge.py```. Cette dernière va effacer les contenus du __data/in_transcription/full_text.txt__ pour qu'on puisse recommencer d'y ajouter des fichiers. Exemple : ```python merge.py erase```

7. Nettoyer et formatter le fichier __data/in_transcription/full_text.txt__ et l'envoyer dans le format XML vers __data/out_transcription/full_text.xml__ avec la fonction ```clean.py```.
![exemple 4](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-01-21.png?raw=true)

	* La fonction ```clean.py``` ne prend pas d'argument. Du coup le fichier d'entrée __data/in_transcription/full_text.txt__ doit se trouver dans le bon endroit et sous son propre nom.

	* ```clean.py``` a besoin d'une librarie ```mypthonlibrary/mylibrary``` et ses deux modules :

		* Le module ```generalFormatting.py``` fournit des fonctions basic_clean() et xml_formatting(). Ces deux fonctions peuvent s'appliquer à peu importe quelle transcription en format TEXT qui conforme aux normes décrites dans l'étape 5.

		* Par contre, le module ```nameFormatting.py``` agit sur une liste de noms qui est écrite directement dans le programme ```clean.py```. Ce module, son dictionnaire et sa commande format_name() sont donc calibrés spécifiquement pour les chapitres XI et XII de _Daniella_. Cependant, le dictionnaire et l'architecture de la fonction format_name() peuvent être adpatés pour des autres documents.
