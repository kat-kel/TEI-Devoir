import re

# chemin de fichier original, uniquement lire, ne le modifiez pas
ORIGINAL = 'data/XMLeScriptorium/19_janvier_1.txt'

# chemin de fichier pour le texte modifié
VERSION = 'transcriptions/test.txt' 

# fichier pour documenter nos modifications
DOC = 'transcriptions/modifications.txt'

# liste d'expressions régulières souhaitées
BAD_APOSTROPHE = re.compile(r"’") # le mauvais unicode pour l'apostrophe standardisée, U+2019
GOOD_APOSTROPHE = "'" # le bon unicode pour l'apostrophe, unicode U+0027
BAD_PUNCTUATION_TWO_PART_START = re.compile(r"([\«\»\!\?\%\$\#])\b") # les signes de ponctuation doubles au début
BAD_PUNCTUATION_TWO_PART_END = re.compile(r"\b([\«\»\!\?\%\$\#])") # les signes de ponctuation doubles à la fin
FIX_PUNCTUATION_TWO_PART = " "
PUNCTUATION_SIMPLE = re.compile(r"\b[\.\,]") #les signes de ponctuation simples
FIX_PUNCTUATION_SIMPLE = ""

def main():
    """
    La fonction main prend un fichier texte et renvoie une version modifiée vers un nouveau chemin, afin de conserver la version originale. Les modifications ont pour but de nettoyer le texte et de le rendre en conformité.

    Les conventions d'écriture ciblées sont :
        1. Toutes les apostrophes doivent être identiques, selon l'unicode U+0027 ; pas le guillemet-apostrophe unicode U+2019 par exemple.
        2. Avant et après chaque signe de ponctuation double (: ; « » ! ? % $ #) se trouve forcement un espace.
        3. Avant chaque signe de ponctuation simple (. ,) il n'y a pas d'espace.
    """
    modifications = [] # liste vide pour documenter nos modifications
    reader = read_file(ORIGINAL) # créer un objet itérable du fichier texte
    modifications = regex(sub_regex, # fonction pour remplaçer une chaîne
                            reader, # la version première d'objet texte itérable
                            VERSION, # chemin de fichier pour stocker le texte modifié
                            BAD_APOSTROPHE, # pattern recherché
                            GOOD_APOSTROPHE, # remplaçement
                            modifications) # documentation de nos modifications
    reader = read_file(VERSION)
    modifications = regex(group_regex_end, # fonction pour remplaçer un groupe
                            reader, # la plus récente version d'objet texte itérable
                            VERSION, # chemin de fichier pour stocker le texte modifié
                            BAD_PUNCTUATION_TWO_PART_END, # pattern recherché
                            FIX_PUNCTUATION_TWO_PART, # remplaçement
                            modifications) # documentation de nos modifications
    reader = read_file(VERSION)
    modifications = regex(group_regex_start, # fonction pour remplaçer un groupe
                            reader, # la plus récente version d'objet texte itérable
                            VERSION, # chemin de fichier pour stocker le texte modifié
                            BAD_PUNCTUATION_TWO_PART_START, # pattern recherché
                            FIX_PUNCTUATION_TWO_PART, # remplaçement
                            modifications) # documentation de nos modifications
    reader = read_file(VERSION)
    modifications = regex(group_regex_end, # fonction pour remplaçer un groupe
                            reader, # la plus récente version d'objet texte itérable
                            VERSION, # chemin de fichier pour stocker le texte modifié
                            PUNCTUATION_SIMPLE, # pattern recherché
                            FIX_PUNCTUATION_SIMPLE, # remplaçement
                            modifications) # documentation de nos modifications
    reader = read_file(VERSION)
    document_changes(DOC, modifications)

def read_file(path):
    """
    La fonction ouvre un fichier texte via un chemin et transforme chaque ligne du texte en une chaîne de caractères ; chaque ligne fait partie d'une liste qui s'appelle 'reader'.

    paramètres :
        path == le chemin de fichier à lire

    sortie :
        reader == une liste de chaînes de caractères, itérable
    """
    with open(path, 'r', encoding='utf8') as f:
        reader = f.readlines()
        return reader

def regex(regex_function, reading_file, path, pattern, repl, modifications):
    """
    La fonction construit l'architecture exigée pour exécuter les opérations regex en lançant une boucle qui itérère sur chaque ligne de la sortie de la fonction read_file.

    paramètres :
        regex_function == la fonction qui exécute le type d'opération regex recherché
        reading_file == une liste de chaînes, sortie de la fonction read_file
        path == le chemin du fichier où se stocke le texte modifié
        pattern == l'expression regulière recherchée, dans le format de re.compile
        repl == l'expression ou chaîne qui va remplacer le pattern
        modifications == une liste de chaînes pour documentater les modifications

    sortie : 
        la liste 'modifications' mise à jour
    """
    line_number = 0
    with open(path, 'w', encoding='utf8') as f:
        for line in reading_file:
            line_number += 1
            if re.search(pattern, line):
                match = re.search(pattern, line)
                new_line = regex_function(pattern, repl, line, match)
                f.write(new_line)
                modifications.append({"line": line_number, "span": match.span(), "match": match.group()})
            else:
                f.write(line)
    return modifications

def sub_regex(pattern, repl, string, match):
    """
    La fonction substitue l'expression recherchée ('pattern') dans une chaîne ('string') avec le remplaçement souhaite'('repl').

    paramètres :
        pattern ==  la sortie de l'opération re.compile() stockée dans un constant
        repl == soit la sortie de l'opération re.compile() ou une chaîne simple stockée dans un constant
        string == la chaîne actuelle de la boucle de la fonction regex()
        match == cette fonction n'utilise pas cet argument, qui est le premier résultat de la boucle parente de cette fonction sortant de re.search(pattern, line); cependant le paramètre est exigé pour que l'alias de cette fonction ('regex_function') convient aux autre fonctions sécondaires, par exemple 'group_regex'

    sortie :
        une chaîne de caractères modifiée ('new_line') destinée à être écrit dans le fichier via la fonction parente regex()
    """
    new_line = re.sub(pattern, repl, string)
    return new_line

def group_regex_end(pattern, repl, string, match):
    """
    La fonction substitue l'expression recherchée ('pattern') avec le remplaçement ('repl') dans la chaîne ('string')

    paramètres :
        pattern ==  la sortie de l'opération re.compile() stockée dans un constant
        repl == soit la sortie de l'opération re.compile() ou une chaîne simple stockée dans un constant
        string == la chaîne actuelle de la boucle de la fonction regex()
        match == le résultat de la boucle de la fonction parente, sortant de la fonction re.search(pattern, line)

    sortie :
        une chaîne de caractères modifiée ('new_line') destinée à être écrit dans le fichier via la fonction parente regex()
    """
    new_line = re.sub(pattern, "{fix}{match}".format(fix=repl, match=match.group(0)), string) # pour les signes de ponctuations exigéants un espace ('fix') avant
    return new_line

def group_regex_start(pattern, repl, string, match):
    """
    La fonction substitue l'expression recherchée ('pattern') avec le remplaçement ('repl') dans la chaîne ('string')

    paramètres :
        pattern ==  la sortie de l'opération re.compile() stockée dans un constant
        repl == soit la sortie de l'opération re.compile() ou une chaîne simple stockée dans un constant
        string == la chaîne actuelle de la boucle de la fonction regex()

    sortie :
        une chaîne de caractères modifiée ('new_line') destinée à être écrit dans le fichier via la fonction parente regex()
    """
    new_line = re.sub(pattern, "{match}{fix}".format(fix=repl, match=match.group(0)), string) # pour les signes de ponctuations exigéants un espace ('fix') après
    return new_line


def document_changes(path, list):
    """
    La fonction écrit la liste de modifications dans un fichier .txt pour que chaque item de la liste (un dictionnaire) commence une nouvelle ligne.

    paramètres :
        path == le chemin où se trouve le fichier pour documenter les modifications faites par les autres fonctions
        liste == la liste de chaînes 'modifications'

    sortie :
        rien
    """
    with open(path, 'w', encoding='utf8') as f:
        for item in list:
            f.write(str(item) + '\n')

if __name__ == "__main__":
    main()