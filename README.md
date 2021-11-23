# TEI-Devoir

## [Consignes de l'évaluation : github.com/Segolene-Albouy](https://github.com/Segolene-Albouy/XML-TEI_M2TNAH/blob/main/ConsignesEvaluation.md)

### Sujet — Roman feuilleton : [Georges Sand, *Daniella*, La Presse](https://gallica.bnf.fr/html/und/presse-et-revues/la-daniella?mode=desktop)

* Télécharger le texte via l’interface de Gallica ;
* Nettoyer le texte (doubles espaces, problème sur les caractères accentués, coquilles…) ;
* Structurer le texte ;
* Signaler dans le texte les noms de personnages et les noms de lieux ;
* Faire un index des noms de personnages et de lieux ;
* Compléter le `teiHeader` ;
* Écrire l’ODD la plus restrictive possible en fonction de votre encodage ;
* Ajouter dans votre ODD la documentation sur votre projet d’encodage, les éléments que vous avez encodés : pourquoi et comment, et quels pourront être à terme les usages de votre édition.

### Consignes générales

* Structurer en XML-TEI votre texte en vue d’une édition et en respectant le genre auquel appartient votre extrait **(/6)** ;

* Compléter de la manière la plus précise possible le `teiHeader` de votre édition, en fonction des éléments nécessaires à son établissement et à la compréhension du texte **(/4)** ;

* Écrire une ODD adaptée à votre encodage et documentée **(/10)** :
	- Générer une ODD à partir de `Roma` ou de `oddbyexample` (/1) ;
	- Votre ODD doit contenir au moins :
		- Une règle contraignant l’usage d’un attribut et sa ou ses valeurs (/1) ;
		- Une règle contraignant l’enchaînement de certains éléments (/1) ;
		- Une règle contraignant la valeur d’un attribut ou l’usage d’un élément ou d’un attribut en fonction de son environnement (/1).
	- À partir de votre ODD, générer la documentation HTML de votre projet :
		- Présenter en introduction votre projet et ses exploitations possibles (/3) ;
		- Documenter le fonctionnement de votre encodage et vos choix de balises (/3).
    
## Méthode

### 1. Télécharger les images de texte.

1. Sélectionner et télécharger le feuilleton en haut résolution (jpg).

2. Stocker ces images sous ```data/images```.
 
### 2. Traduire les images de texte en fichiers de texte (Tesseract OCR).

1. [Suivre les instruction d'installation](https://tesseract-ocr.github.io/tessdoc/Installation.html).

  ```sudo apt install tesseract-ocr```

  ```sudo apt install libtesseract-dev```

  - [_télécharger les données linguistiques entraînées, AppImage_](https://github.com/AlexanderP/tesseract-appimage/releases)

  ```chmod a+x tesseract*.AppImage```

2. Démarrer Tesseract sur les images de texte.
  - _noter le chemin de tesseract*.AppImage_ (CHEMIN_AppImage)
  - _noter le chemin d'image à traiter_ (CHEMIN_image)
  - _noter le chemin d'où se placera le nouveau fichier_ (CHEMIN_fichier)
  - pour créer un fichier txt :

    ```CHEMIN_AppImage/tesseract*.AppImage -l fra CHEMIN_image.jpg CHEMIN_fichier```

  - pour créer un fichier pdf searchable :
    ```CHEMIN_AppImage/tesseract*.AppImage -l fra CHEMIN_image.jpg CHEMIN_fichier pdf```

### 3. Nettoyer les fichiers de texte.

1. En lisant les images de texte, corriger à la main les fichiers de texte automatisés.

  - Méthode de corréction :
    - marquer les mots en italique avec \_l'underscore_
    - garder les coquilles, en les marquant avec \[sic]
    
2. Nettoyer les transcriptions préliminaires sur RegEx.

  1. **Copier-coller uniquement le body du texte dans le TEST STRING du site https://regex101.com**

  2. **Supprimer les epaces à la fin de lignes, pour que chaque ligne termine avec une saute de ligne.**
    - sélectionner les espaces avec l'expression : ( )$
    - remplacer avec rien 

  3. **Marquer le début de chaque paragraphe avec la balise <p>.**
    - sélectionner le début de paragraphes avec l'expression : \n\n(^.)
    - remplacer avec : \n\n<p>$1

  4. **Mettre manuellement la balise <p> au début du texte pour qu'il conforme au reste.**

  5. **Marquer la fin de chaque paragraphe avec la balise </p>.**
    - sélectionner la fin de paragraphes avec l'expression : (.)\\n\\n
    - remplacer avec : $1</p>\\n\\n

  6. **Mettre manuellement la balise fermante </p> à la fin du dernier paragraphe pour qu'il conforme aux autres.**

  7. **Standardiser les apostrophes.**
    - sélectionner les apostrophes spéciales avec l'expression : ’
    - remplacer avec : '

  8. **Standardiser les espaces entre les lettres et la ponctuation.**
    - sélectionner la ponctuation qui suit les espaces avec l'expression : \\b ([\\!\\.\\,\\;\\:])
    - remplacer avec : \$1

  9. **Standardiser les espaces entre les lettres et les guillemets.**
    - sélectionner les citations avec l'expression : \\»\\«\\

  - Remplacer les premiers indicateurs de l'italique avec la propre balise.
    - sélectionner le premier \_ avec l'expression : (\_)\B
    - remplacer avec : \<hi rend="italic">

  - Remplacer les derniers indicateurs de l'italique avec la propre balise.
    - sélectionner le _ restant qui doit forcement être à la fin avec l'expression : (_)
    - remplacer avec : \</hi>
