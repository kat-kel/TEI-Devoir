# TEI-Devoir

[Consignes de l'évaluation : github.com/Segolene-Albouy](https://github.com/Segolene-Albouy/XML-TEI_M2TNAH/blob/main/ConsignesEvaluation.md)

#### Sujet — Roman feuilleton : [Georges Sand, *Daniella*, La Presse](https://gallica.bnf.fr/html/und/presse-et-revues/la-daniella?mode=desktop)

* Télécharger le texte via l’interface de Gallica ;
* Nettoyer le texte (doubles espaces, problème sur les caractères accentués, coquilles…) ;
* Structurer le texte ;
* Signaler dans le texte les noms de personnages et les noms de lieux ;
* Faire un index des noms de personnages et de lieux ;
* Compléter le `teiHeader` ;
* Écrire l’ODD la plus restrictive possible en fonction de votre encodage ;
* Ajouter dans votre ODD la documentation sur votre projet d’encodage, les éléments que vous avez encodés : pourquoi et comment, et quels pourront être à terme les usages de votre édition.

#### Consignes générales

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
    
# Ma Méthode

## Nettoyer le texte

1. Télécharger une image JPEG en haute résolution de Gallica qui extrait uniquement le contenu du feuilleton.
	* Cette méthode est conseillée parce que la qualité d'image du périodique, même si elle sorte de l'IIIF, est trop faible pour être bien lue par le logiciel eScriptorium.
2. Transformer le JPEG en PDF. (J'ai utilisé le logiciel Tesseract.)
3. Transcrire dans eScriptorium le fichier PDF, selon les normes ci-dessous, et sortir la transcription d'un format TEXT.
	* Pour toute occurence de mots en italique, elle est entournée par un double underscore, "\__\\_exemple_\__"
	* Si le texte imprimé présente un erreur typographique bien lisible, il est conservé et il est suivi par \[sic], mais les erreurs orthographiques ne sont pas marqués
	* Si le texte imprimé manque un mot ou une lettre attendu, il est ajouté entre crochets, "C'es\[t] fait."
4. Passer cette transcription brute dans le programme que j'ai écrit qui s'appelle 'clean.py'
	* Ce programme python a besoin de pacquets ```re``` et ```click```