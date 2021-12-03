import re

# un dictionnaire d'objets motifs, des 'Patterns", sortants d'une expression régulière pour capturer certaines chaînes ciblées
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

# un dictionnaire de chaînes de caractères, des 'Strings' ; elles seront envoyées soit dans la place d'une chaîne existante soit à côté d'une chaîne existante
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

# un dictionnaire de personnages
dictNames = {
    # versions possibles : Daniella, Frascatine
    'find Daniella': re.compile(r"((?:Daniella)|(?:Frascatine))")
    ,
    # versions possibles : Médora, Medora, m/Miss Médora, m/Miss Medora
    'find Medora': re.compile(r"((?:Médora)|(?:([m|M]iss) (Médora)))")
    ,
    # versions  possibles: Harriet, l/Lady Harriet
    'find Harriet': re.compile(r"((?:Harriet)|(?:([l|L]ady) (Harriet)))")
    ,
    # versions possibles : l/Lord B***
    'find Lord B': re.compile(r"(?:([l|L]ord) (B\*\*\*))")
    ,
    # versions possibles : l/Lady B***
    'find Lady B': re.compile(r"(?:([l|L]ady) (B\*\*\*))")
    ,
    # versions possibles : Jean Valreg
    'find Valreg': re.compile(r"(?:(Jean) (Valreg))")
    ,
    # lieux à rechercher
    'find Frascati': re.compile(r"(?:Frascati)[\s|\.|\,]")
    ,
    'find Rome': re.compile(r"(?:Rome)\s")
    ,
    'find Tartaglia': re.compile(r"(?:Tartaglia)\s")
    ,
    # les id
    'id Daniella': '<persName ref="Dan">'
    ,
    'id Medora': '<persName ref="Med">'
    ,
    'id Harriet': '<persName ref="Har">'
    ,
    'id Lord B': '<persName ref="Lord B">'
    ,
    'id Lady B': '<persName ref="Lady B">'
    ,
    'id Valreg': '<persName ref="Valreg">'
    ,
    'id Frascati': '<placeName ref="Fras">'
    ,
    'id Rome': '<placeName ref="Rome">'
    ,
    'id Tartaglia': '<placeName ref="Tart">'
    ,
}


def format_forename(name, line):
    find_key = 'find {}'.format(name)
    id_key = 'id {}'.format(name)
    name_keys = [find_key, id_key]
    if re.search(dictNames[name_keys[0]], line):
        match = re.findall(dictNames[name_keys[0]], line)
        for i in match:
            if isinstance(i, str): #si le résultat n'est qu'une chaîne, ex. Daniella
                line = re.sub(dictNames[name_keys[0]], '{persName}{tag1}{name}{tag2}'.format(persName=dictNames[name_keys[1]], tag1='<surname>', name=i, tag2='</surname>'), line)
            elif i[1] == '': # si l'instance du nom ne se précède pas par un honorific
                # ex. <persName ref="Med"><forename>Médora</forename></persName>
                line = re.sub(dictNames[name_keys[0]], '{persName}{tag1}{name}{tag2}'.format(persName=dictNames[name_keys[1]], tag1='<forename>', name=i[0], tag2='</forename></persName>'), line)
            else: # si l'instance du nom se précède par un honorific
                # ex. <persName ref="Med"><addName type="honorific"><Miss</addName><forename>Médora</forename></persName>
                line = re.sub(dictNames[name_keys[0]], '{persName}{tag1}{honorific}{tag2}{tag3}{name}{tag4}'.format(persName=dictNames[name_keys[1]], tag1='<addName type="honorific">', honorific=i[1], tag2='</addName>', tag3='<forename>', name=i[2], tag4='</forename></persName>'), line)
    return(line)

def format_surname(name, line):
    find_key = 'find {}'.format(name)
    id_key = 'id {}'.format(name)
    name_keys = [find_key, id_key]
    if re.search(dictNames[name_keys[0]], line):
        match = re.findall(dictNames[name_keys[0]], line)
        for i in match:
            if i[1] == '': # si l'instance du nom ne se précède pas par un honorific
                line = re.sub(dictNames[name_keys[0]], '{persName}{tag1}{name}{tag2}'.format(persName=dictNames[name_keys[1]], tag1='<surname>', name=i[0], tag2='</surname></persName>'), line)
            else: # si l'instance du nom se précède par un honorific
                # ex. <persName ref="Lord B"><addName type="honorific"><Lord</addName><forename>B***</forename></persName>
                line = re.sub(dictNames[name_keys[0]], '{persName}{tag1}{honorific}{tag2}{tag3}{name}{tag4}'.format(persName=dictNames[name_keys[1]], tag1='<addName type="honorific">', honorific=i[0], tag2='</addName>', tag3='<surname>', name=i[1], tag4='</surname></persName>'), line)
    return(line)

def format_fullName(name, line):
    find_key = 'find {}'.format(name)
    id_key = 'id {}'.format(name)
    name_keys = [find_key, id_key]
    if re.search(dictNames[name_keys[0]], line):
        match = re.finditer(dictNames[name_keys[0]], line)
        for i in match:
            line = re.sub(dictNames[name_keys[0]], '{persName}{tag1}{forename}{tag2}{tag3}{surname}{tag4}'.format(persName=dictNames[name_keys[1]], tag1='<forename>', forename=i[1], tag2='</forename>', tag3='<surname>', surname=i[2], tag4='</surname></persName>'), line)
    return(line)

def format_placeName(name, line):
    find_key = 'find {}'.format(name)
    id_key = 'id {}'.format(name)
    name_keys = [find_key, id_key]
    if re.search(dictNames[name_keys[0]], line):
        match = re.finditer(dictNames[name_keys[0]], line)
        for i in match:
            line = re.sub(dictNames[name_keys[0]], '{tag1}{name}{tag2}'.format(tag1=dictNames[name_keys[1]], name=i[0], tag2='</placeName>'), line)
    return(line)