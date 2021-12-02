import re
import click

@click.command()
@click.option('--fichier', help='entrez le nom de fichier texte brut à formatter, sans le .txt')
@click.argument('fichier')
def main(fichier):
    """
    DOCUMENTATION :
	    La fonction main prend un fichier texte et renvoie une version modifiée vers un nouveau chemin, afin de conserver la version originale. Les modifications ont pour but de nettoyer le texte et de le rendre en conformité.

	    Le texte entrée dans la fonction doit conformer au modèle décrit dessous. Notamment il aura des diacritiques d'une langue latin et il gardera des sauts de ligne. Les mots en italique doivent être marqués devant et derrière par deux underscores. Si une expression en italique traverse plusieurs lignes, l'underscore fermant doit apparaître à la fin de l'expression, donc pas à la fin de ligne si le mot continue à la prochaine.
		| contre-partie de celle que j’ai surprise à la __Ré-
		| serve__. Il paraît que je suis destiné à m’emparer,

	    En outre certains moyens de marquer des coquilles dans la source transcrite doivent conformer aux deux règles suivantes.
		(1) Les expressions dont le mot ou la lettre est corrumpu sont corrigées en plaçant la correction entre crochets []. Le texte envoyé vers cette fonction devrait corriger uniquement les mots et les lettres illisbles, et pas les mauvaises orthographes.
		| — Il n’y a rien là pour la [vue], continua le ci-
		# Dans cet exemple ci-dessus, le mot 'vue' devrait être présente dans la phrase mais il n'était pas lisible dans la source.
	    (2) Les expressions dont une coquille est bien lisible dans la source sont suivies par le mot latin 'sic' entre crochets.
		| huttes de paille, assez vastes pour abriter.[sic] la
		# Dans cet exemple ci-dessus, le point suivi par [sic] a été imprimé en erreur, mais cet erreur est conservé dans la transcription envoyé vers cette fonction.

	    En résumé, les conventions typographiques ciblées sont les suivants :
		1. Toutes les apostrophes doivent être identiques, selon l'unicode U+0027, et pas par exemple le guillemet-apostrophe unicode U+2019.
		2. Avant et après chaque signe de ponctuation double (: ; « » ! ? % $ #) se trouve forcement un espace.
		3. Avant chaque signe de ponctuation simple (. ,) il n'y a pas d'espace.
		4. Les expressions ou mots en italique doivent être mises entre les balises d'XML <hi rend="italic"> et </hi>.
		5. Les coquilles suivies par [sic] doivent être mises entre les balises <sic> et </sic>.
		6. Les corrections entre crochets doivent être mises entre deux sets de balises : <choice><corr> et </corr><sic></sic></choice>.
    """
    
    # identifier le chemin du fichier de départ ; ne le modifiez pas ! ce fichier sera ouvert uniquement dans un mode de lecture
    original = 'data/XMLeScriptorium/{}.txt'.format(fichier)
    # transformer le fichier où se trouve la transcription originale en un objet itérable, ce qui s'appelle le 'reader' 
    reader = read_file(original)

    # identifier le chemin du fichier où le texte modifié se trouvera
    version = 'transcriptions/{}.txt'.format(fichier) 
    # préparer le nouveau fichier en supprimant les anciennes modifications s'il y en a dans le fichier, pour qu'il soit vide au début de la fonction
    version = empty_version(version)

    # en lisant chaque ligne du texte (celle qui est téchniquement un item de la liste de chaînes du 'reader') modifier cette chaîne et la écrire dans le fichier ouvert en mode d'ecriture, qui s'appelle 'f' dans la boucle ci-dessous mais 'version' dans la fonction main()
    with open(version, 'w', encoding='utf8') as f:
        for line in reader:
            # nettoyer les lignes de texte suivant les trois premiers normes listées au-dessus
            clean_line = basic_clean(line)
            # formatter les lignes de texte suivant les trois derniers normes listées au-dessus
            formatted_line = xml_elements(clean_line)
            # écrire la ligne modifié dans le fichier ouvert en mode d'écriture 'version'
            f.write(formatted_line)

# un dictionnaire global d'objets motifs, des 'Patterns", sortants d'une expression régulière pour capturer certaines chaînes ciblées
dictPattern = {
    'empty space at start of line': re.compile(r"(^\s)+"),
    'bad apostrophe': re.compile(r"’"),
    'space missing between two-part punctuation and word': re.compile(r"([\:\;\«\!\?\%\$\#])\b"),
    'space missing between word and two-part punctuation': re.compile(r"\b([\:\;\»\!\?\%\$\#])"),
    'extra space before simple punctuation': re.compile(r"\s[\.\,]"),
    'double underscore and content between': re.compile(r"(__)([^__]+)(__)"), # (groupe 1 de l'objet de correspondance: premier underscore)(groupe 2 de l'objet de correspondance: contenu en italique)(groupe 3 de l'objet de correspondance: deuxième underscore)
    'continuing italic word at end of line': re.compile(r"(__)(.+)"), # (groupe 1 de l'objet de correspondance: premier underscore)(groupe 2 de l'objet de correspondance: contenu en italique)
    'continued italic word at start of line': re.compile(r"(.+)(__)"), # (groupe 1 de l'objet de correspondance: contenu en italique)(groupe 2 de l'objet de correspondance: dernier underscore)
    'sic in brackets': re.compile(r"(\S+)(\[sic\])"), # (groupe 1 de l'objet de correspondance: le contenu avant le marqueur [sic])(groupe 2 de l'objet de correspondance: les crochets [sic])
    'correction': re.compile(r"(\[.+\])"),
    }
# un dictionnaire global de chaînes de caractères, des 'Strings' ; elles seront envoyées soit dans la place d'une chaîne existante soit à côté d'une chaîne existante
dictString = {
        'good apostrophe': "'",
        'one space': ' ',
        'no space': '',
        'first italics tag': '<hi rend="italic">',
        'last italics tag': '</hi>',
        'first sic tag': '<sic>',
        'last sic tag': '</sic>',
        'first correction tags': '<choice><corr>',
        'last correction tags': '</corr><sic></sic></choice>'
    }

def basic_clean(line):
    """
    DOCUMENTATION :
        La fonction devrait nettoyer une ligne du fichier texte selon les normes souhaitées. Dans ce cas, je lui ai assigné trois normes de proprété :
            1. Toutes les apostrophes doivent être identiques, selon l'unicode U+0027, et pas par exemple le guillemet-apostrophe unicode U+2019.
            2. Avant et après chaque signe de ponctuation double (: ; « » ! ? % $ #) se trouve forcement un espace.
            3. Avant chaque signe de ponctuation simple (. ,) il n'y a pas d'espace.

        paramètres :
            new_line == la chaîne de caractères passée dans la boucle de la fonction parente, donc une ligne de l'objet 'reader' 

        sortie :
            new_line == une chaîne modifiée destinée pour la prochaine fonction de la boucle, ce qui la rendre en conformité aux normes d'XML
    """
    # effacer les espaces au début de ligne
    new_line = re.sub(dictPattern['empty space at start of line'], dictString['no space'], line)
    # remplacer tous les guillements-apostrophes avec une apostrophe
    new_line = re.sub(dictPattern['bad apostrophe'], dictString['good apostrophe'], new_line)
    # insérer un espace entre une signe de ponctuation et un mot, ": exemple"
    new_line = re.sub(dictPattern['space missing between two-part punctuation and word'], dictString['one space'], new_line)
    # insérer un espace entre un mot et une signe de ponctuation, "exemple :"
    new_line = re.sub(dictPattern['space missing between word and two-part punctuation'], dictString['one space'], new_line)
    # supprimer un espace entre un mot et une signe de ponctuation, "exemple."
    new_line = re.sub(dictPattern['extra space before simple punctuation'], dictString['no space'], new_line)
    return new_line

def xml_elements(new_line):
    """
    DOCUMENTATION :
        La fonction devrait formatter une ligne du fichier texte selon les normes souhaitées. Dans ce cas, je lui ai assigné trois normes d'XML :
            1. Les expressions ou mots en italique doivent être mises entre les balises d'XML <hi rend="italic"> et </hi>.
            2. Les coquilles suivies par [sic] doivent être mises entre les balises <sic> et </sic>.
            3. Les corrections entre crochets doivent être mises entre deux sets de balises : <choice><corr> et </corr><sic></sic></choice>.

        paramètres :
            new_line == la chaîne de caractères sortante de la fonction précédente qui l'a nettoyée

        sortie :
            new_line == une chaîne modifiée destinée pour la prochaine fonction de la boucle, ce qui l'utilise pour écrire une nouvelle ligne dans la fichier 'version'
    """
# mettre les expressions ou mots en italique entre les balises d'XML <hi rend="italic"> et </hi>
    if re.search(dictPattern['double underscore and content between'], new_line) :
        match = re.search(dictPattern['double underscore and content between'], new_line)
        new_line = re.sub(dictPattern['double underscore and content between'], "{tag1}{match}{tag2}".format(tag1=dictString['first italics tag'], match=match.group(2), tag2=dictString['last italics tag']), new_line)
    elif re.search(dictPattern['continuing italic word at end of line'], new_line):
        match = re.search(dictPattern['continuing italic word at end of line'], new_line)
        new_line = re.sub(dictPattern['continuing italic word at end of line'], "{tag}{match}".format(tag=dictString['first italics tag'], match=match.group(2)), new_line)
    elif re.search(dictPattern['continued italic word at start of line'], new_line):
        match = re.search(dictPattern['continued italic word at start of line'], new_line)
        new_line = re.su(dictPattern['continued italic word at start of line'], "{match}{tag}".format(match=match.group(1), tag=dictString['last italics tag']), new_line)
    else:
        pass
    # mettre les coquilles suivies par [sic] entre les balises <sic> et </sic>
    if re.search(dictPattern['sic in brackets'], new_line):
        match = re.search(dictPattern['sic in brackets'], new_line)
        new_line = re.sub(dictPattern['sic in brackets'], "{tag1}{match}{tag2}".format(tag1=dictString['first sic tag'], match=match.group(1), tag2=dictString['last sic tag']), new_line)
    else:
        pass
    # mettre les corrections entre deux sets de balises : <choice><corr> et </corr><sic></sic></choice>
    if re.search(dictPattern['correction'], new_line):
        match = re.search(dictPattern['correction'], new_line)
        new_line = re.sub(dictPattern['correction'], "{tag1}{match}{tag2}".format(tag1=dictString['first correction tags'], match=match.group(0), tag2=dictString['last correction tags']), new_line)
    else:
        pass
    return new_line

def empty_version(version):
    """
    DOCUMENTATION :
    	La fonction ouvre le fichier où se stockera le nouveau texte et efacer ses contenus s'il y en a
    """
    with open(version, 'w') as f:
        pass
    return version

def read_file(path):
    """
    DOCUMENTATION :
	    La fonction ouvre un fichier en mode de lecture et transforme chaque ligne du texte en une chaîne de caractères ; chaque ligne devient un item dans une liste qui s'appelle 'reader'.

	    paramètres :
		    path == le chemin de fichier à lire

	    sortie :
		    reader == une liste de chaînes de caractères, itérable
    """
    with open(path, 'r', encoding='utf8') as f:
        reader = f.readlines()
        return reader

if __name__ == "__main__":
    main()
