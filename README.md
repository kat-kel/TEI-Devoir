# TEI-Devoir

[Consignes de l'évaluation : github.com/Segolene-Albouy](https://github.com/Segolene-Albouy/XML-TEI_M2TNAH/blob/main/ConsignesEvaluation.md)

    
# Ma Méthode

## Nettoyer le texte

1. Télécharger une image JPEG en haute résolution de Gallica qui extrait uniquement le contenu du feuilleton.

2. Transformer le JPEG en PDF. (Moi, j'ai utilisé le logiciel Tesseract)

3. Transcrire dans eScriptorium le fichier PDF, en notant dans un fichier à part des mots en italiques et des coquilles.

4. Sortir de l'eScriptorium un fichier TEXT et le stocker dans __data/out_eScriptorium__.
![exemple 1](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-03-47.png?raw=true)

5. Faire des petites modifications à la main et sauvgarder les transcriptions modifiés dans le sous-dossier __data/in_transcription__.
![exemple 2](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-03-01.png?raw=true)

	* D'après les notes prises lors de la transcription dans eScriptorium :

		* Entourner des mots en italique par deux underscores
		* Suivre des coquilles avec \[sic]
		* Entourner par des crochets des corrections des lettres et/ou des mots illisibles, e emple --> e\[x]emple

	* Récupérer les paragraphes de l'imprimé :

		* Pour fusionner des mots divisés à la fin d'une ligne, sélectionner ```(-)\n``` et le remplacer avec rien.

		* Pour fusionner des phrases qui traversent des lignes, sélectionner ```(\b|[__]|\,|\;)\n``` et le remplacer avec ```$1 ```, avec un espace à la fin qui remplacera le saut de ligne.

		* Mais si le texte d'origine ne contient pas d'espaces pour diviser des paragraphes--comme celui qui sort de l'eScriptorium--cette méthode se trompera sur les phrases qui commencent une ligne mais pas un nouveau paragraphe. Il faut donc vérifier avec l'image transcrite que les lignes de texte représentent les paragraphes.

6. Passer tous les fichiers de __data/in_transcription__ dans la fonction ```add``` du programme ```merge.py```, qui va les combiner dans le fichier __data/in_transcription/full_text.txt__. La fonction créera ce dernier fichier s'il n'existe pas déjà. D'ailleurs, il faut éxecuter la fonction ```add``` sur des fichiers dans leur propre ordre.
![exemple 3](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-02-24.png?raw=true)

	* La fonction ```add``` de ```merge.py``` exige deux arguments dans l'ordre suivant : (1) le nom du fichiers (sans .txt) qui doit forcement se trouver dans __data/in_transcription__, (2) l'id de la source (l'id devrait être court)

	* La fonction avec ces deux arguments se ressemblera à celui ci-dessous :

	```python merge.py add 19_janvier_1 19Jan```

	> Cet exemple de commande dans le terminal démarrera la fonction ```add``` et ensuite récrira le fichier __data/in_transcription/19_janvier_1.txt__ vers __data/in_transcription/full_text.txt__ avec des modifications de l'XML. De plus, elle lui donnera l'id "19Jan" qui servira à l'encodage XML.

	* S'il y a déjà des données récrites dans le fichier __data/in_transcription/full_text.txt__, la fonction ```add``` le reconnaîtra et ajoutera le nouveau à la fin, en gardant <\body> en haut et <\\body> en bas. Par contre, la fonction compte sur l'utilisateur d'ajouter des fichiers dans leur propre ordre.

	* Dans le cas où s'effectue un erreur d'utilisateur, il est recommandé d'appeller la fonction ```erase``` du programme ```merge.py```. Cette dernière va effacer les contenus du __data/in_transcription/full_text.txt__ pour qu'on puisse recommencer d'y ajouter des fichiers.

7. Nettoyer et formatter le fichier __data/in_transcription/full_text.txt__ et l'envoyer dans le format XML vers __data/out_transcription/full_text.xml__ avec la fonction ```clean.py```.
![exemple 4](https://github.com/kat-kel/TEI-Devoir/blob/main/Capture%20d%E2%80%99%C3%A9cran%20de%202021-12-08%2020-01-21.png?raw=true)

	* La fonction ```clean.py``` ne prend pas d'argument. Du coup le fichier d'entrée __data/in_transcription/full_text.txt__ doit se trouver dans le bon endroit et sous son propre nom.

	* ```clean.py``` a besoin d'une librarie ```mypthonlibrary/mylibrary``` et ses deux modules :

		* Le module ```generalFormatting.py``` fournit des fonctions basic_clean() et xml_formatting(). Ces deux fonctions peuvent s'appliquer à peu importe quelle transcription en format TEXT qui conforme aux normes décrites dans l'étape 5.

		* Par contre, le module ```nameFormatting.py``` agit sur une liste de noms qui est écrite directement dans le programme ```clean.py```. Ce module, son dictionnaire et sa commande format_name() sont donc calibrés spécifiquement pour les chapitres XI et XII de _Daniella_. Cependant, le dictionnaire et l'architecture de la fonction format_name() peuvent être adpatés pour des autres documents.

## Faire des index et compléter le ```teiHeader```
1. à voir

## Écrire l'ODD
1. à voir
