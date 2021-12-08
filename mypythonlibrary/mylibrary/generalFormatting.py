import re

# un dictionnaire d'objets motifs, des 'Patterns", sortants d'une expression régulière pour capturer certaines chaînes ciblées
dictPattern = {
    'empty space at start of line': re.compile(r"(^\s)+"), # trouve un object motif qui sera remplacé par une chaîne
    'two spaces': re.compile(r"  "), # trouve un object motif qui sera remplacé par une chaîne
    'bad apostrophe': re.compile(r"’"), # trouve un object motif qui sera remplacé par une chaîne
    'space missing between two-part punctuation and word': re.compile(r"([\:\;\«\!\?\%\$\#])\b"), # trouve un object motif qui sera réutilisé dans une nouvelle chaîne, "{object}{chaîne}"
    'space missing between word and two-part punctuation': re.compile(r"\b([\:\;\»\!\?\%\$\#])"), # trouve un object motif qui sera réutilisé dans une nouvelle chaîne, "{chaîne}{object}"
    'extra space before simple punctuation': re.compile(r"\s[\.\,]"), # trouve un object motif qui sera remplacé par une chaîne
    'double underscore and content between': re.compile(r"(__)([^__]+)(__)"), # renvoie une liste de tuples ; l'item à garder est le deuxième
    'sic in brackets': re.compile(r"(\S+)(\[sic\])"), # renvoie une liste de tuples ; l'item à garder est le premier
    'correction': re.compile(r"\[([^\[]+)\]"), # renvoie une liste de chaînes
    'paragraph': re.compile(r"(^[^<][^A-Z{2,}].+)"),
    'not paragraph': re.compile(r"(([A-Z]{2,}.+)|(?:<body>)|(?:</body>))")
}

# un dictionnaire de chaînes de caractères, des 'Strings' ; elles seront envoyées soit dans la place d'une chaîne existante soit à côté d'une chaîne existante
dictString = {
        'good apostrophe': "'",
        'one space': ' ',
        'no space': '',
        'first italics tag': '<hi rend="italic">',
        'last italics tag': '</hi>',
        'first sic tag': '<sic>',
        'last sic tag': '</sic>',
        'first correction tags': '<choice><sic></sic><corr>',
        'last correction tags': '</corr></choice>'
}

def basic_clean(line):
    """DOCUMENTATION :
        La fonction 'basic_clean' devrait nettoyer une ligne de texte selon les normes souhaitées :
            (1) Toutes les apostrophes doivent être identiques, selon l'unicode U+0027, et pas par exemple le guillemet-apostrophe unicode U+2019.
            (2) Avant et après chaque signe de ponctuation double (: ; « » ! ? % $ #) se trouve forcement un espace.
            (3) Avant chaque signe de ponctuation simple (. ,) il n'y a pas d'espace.

        paramètres :
            new_line == la chaîne de caractères passée dans la boucle de la fonction parente, donc une ligne de l'objet 'reader' 

        sortie :
            new_line == une chaîne modifiée destinée pour la prochaine fonction de la boucle, ce qui la rendra en conformité aux normes d'XML."""
    # effacer les espaces supplémentaires et ceux au début de ligne
    line = re.sub(dictPattern['two spaces'], ' ', line)
    line = re.sub(dictPattern['empty space at start of line'], dictString['no space'], line)
    # remplacer tous les guillements-apostrophes avec une apostrophe
    line = re.sub(dictPattern['bad apostrophe'], dictString['good apostrophe'], line)
    # insérer un espace entre une signe de ponctuation et un mot, ": exemple"
    if re.search(dictPattern['space missing between two-part punctuation and word'], line):
        match_list = re.findall(dictPattern['space missing between two-part punctuation and word'], line)
        # pour autant de fois que la commande .findall a trouvé des objets motifs, modifier uniqument le premier ; cette boucle permet d'éviter que toutes les occurences d'objet motif dans une ligne ne soit pas modifiée avec une solution dérivée de la première occurence mais qui n'est pas convenable aux celles qui suivent
        for i in range(len(match_list)):
            match = re.search(dictPattern['space missing between two-part punctuation and word'], line)
            line = re.sub(dictPattern['space missing between two-part punctuation and word'], "{punctuation}{space}".format(punctuation=match.group(0), space=dictString['one space']), line, 1)
    # insérer un espace entre un mot et une signe de ponctuation, "exemple :"
    if re.search(dictPattern['space missing between word and two-part punctuation'], line):
        match_list = re.findall(dictPattern['space missing between word and two-part punctuation'], line)
        # pour autant de fois que la commande .findall a trouvé des objets motifs, modifier uniqument le premier ; cette boucle permet d'éviter que toutes les occurences d'objet motif dans une ligne ne soit pas modifiée avec une solution dérivée de la première occurence mais qui n'est pas convenable aux celles qui suivent
        for i in range(len(match_list)):
            match = re.search(dictPattern['space missing between word and two-part punctuation'], line)
            line = re.sub(dictPattern['space missing between word and two-part punctuation'], "{space}{punctuation}".format(space=dictString['one space'], punctuation=match.group(0)), line, 1)
    # supprimer un espace entre un mot et une signe de ponctuation, "exemple."
    line = re.sub(dictPattern['extra space before simple punctuation'], dictString['no space'], line)
    return line

def xml_elements(line):
    """DOCUMENTATION :
        La fonction devrait formatter une ligne de texte selon les normes souhaitées :
            (1) Les paragraphes doivent être mises entre les balises d'XML <p> et </p>
            (2) Les expressions ou mots en italique doivent être mises entre les balises d'XML <hi rend="italic"> et </hi>.
            (3) Les coquilles suivies par [sic] doivent être mises entre les balises <sic> et </sic>.
            (4) Les corrections entre crochets doivent être mises entre deux sets de balises : <choice><corr> et </corr><sic></sic></choice>.

        paramètres :
            new_line == la chaîne de caractères sortante de la fonction précédente qui l'a nettoyée

        sortie :
            new_line == la chaîne modifiée destinée pour la prochaine fonction de la boucle, ce qui mettra des balises autour des noms"""

    # (2) s'il y a des mots en italique == <hi rend="italic"> et </hi>
    if re.search(dictPattern['double underscore and content between'], line) :
        match_list = re.findall(dictPattern['double underscore and content between'], line)
        # pour autant de fois que la commande .findall a trouvé des objets motifs, modifier uniqument le premier ; cette boucle permet d'éviter que toutes les occurences d'objet motif dans une ligne ne soit pas modifiée avec une solution dérivée de la première occurence mais qui n'est pas convenable aux celles qui suivent
        for i in range(len(match_list)):
            for match_tuple in match_list:
                line = re.sub(dictPattern['double underscore and content between'], "{tag1}{match}{tag2}".format(tag1=dictString['first italics tag'], match=match_tuple[1], tag2=dictString['last italics tag']), line, 1)

    # (3) coquilles suivies par [sic] == <sic> et </sic>
    if re.search(dictPattern['sic in brackets'], line):
        match_list = re.findall(dictPattern['sic in brackets'], line)
        # pour autant de fois que la commande .findall a trouvé des objets motifs, modifier uniqument le premier ; cette boucle permet d'éviter que toutes les occurences d'objet motif dans une ligne ne soit pas modifiée avec une solution dérivée de la première occurence mais qui n'est pas convenable aux celles qui suivent
        for i in range(len(match_list)):
            for match_tuple in match_list:
                line = re.sub(dictPattern['sic in brackets'], "{tag1}{match}{tag2}".format(tag1=dictString['first sic tag'], match=match_tuple[0], tag2=dictString['last sic tag']), line, 1)

    # (4) corrections == <choice><sic></sic><corr> et </corr></choice>
    if re.search(dictPattern['correction'], line):
        match_list = re.findall(dictPattern['correction'], line)
        # pour autant de fois que la commande .findall a trouvé des objets motifs, modifier uniqument le premier ; cette boucle permet d'éviter que toutes les occurences d'objet motif dans une ligne ne soit pas modifiée avec une solution dérivée de la première occurence mais qui n'est pas convenable aux celles qui suivent
        for i in range(len(match_list)):
            line = re.sub(dictPattern['correction'], "{tag1}{match}{tag2}".format(tag1=dictString['first correction tags'], match=match_list[i], tag2=dictString['last correction tags']), line, 1)
    else:
        pass
    return line