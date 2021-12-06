import re

# un dictionnaire de personnages et des lieux
dictNames = {
    # personnages connus par leurs prénom ; l'expression régulière doit exclure toute occurence dans une ligne déjà mise entre balises
    'forename simple': {
         # versions possibles : Daniella, Frascatine
        'Daniella': re.compile(r"[^(?:>)]((?:Daniella)|(?:Frascatine))")
        },
    'forename with honorific': {
        # versions possibles : Médora, Medora, m/Miss Médora, m/Miss Medora
        'Medora': re.compile(r"[^(?:>)]((?:Médora)|(?:([m|M]iss) (Médora)))"),
        # versions  possibles: Harriet, l/Lady Harriet
        'Harriet': re.compile(r"[^(?:>)]((?:Harriet)|(?:([l|L]ady) (Harriet)))")
    },
    # personnages connus par leurs nom de famille
    'surname': {
        # versions possibles : l/Lord B***
        'Lord B': re.compile(r"[^(?:name>)](?:([l|L]ord) (B\*\*\*))"),
        # versions possibles : l/Lady B***
        'Lady B': re.compile(r"[^(?:name>)](?:([l|L]ady) (B\*\*\*))")
    },
    # personnages connus par leurs prénom et nom de famille
    'fullName': {
        # versions possibles : Jean Valreg
        'Valreg': re.compile(r"[^(?:name>)](?:(Jean) (Valreg))")
    },
    # lieux
    'placeName': {
        'Frascati': re.compile(r"[^(?:name>)](?:Frascati)"),
        'Rome': re.compile(r"(?:Rome)"),
        'Tartaglia': re.compile(r"(?:Tartaglia)")
    },
    # les id
    'id' :{
        'id Daniella': '<persName ref="Dan">',
        'id Medora': '<persName ref="Med">',
        'id Harriet': '<persName ref="Har">',
        'id Lord B': '<persName ref="Lord B">',
        'id Lady B': '<persName ref="Lady B">',
        'id Valreg': '<persName ref="Valreg">',
        'id Frascati': '<placeName ref="Fras">',
        'id Rome': '<placeName ref="Rom">',
        'id Tartaglia': '<placeName ref="Tart">',
        }
    }

def format_name(name, line):
    # si le nom entré dans la fonction appartient à un personnage connu par son prénom
    for key in dictNames['forename simple']:
        if key == name:
            id = 'id {}'.format(name)
            find_name = name
            name_keys = [find_name, id]
            if re.search(dictNames['forename simple'][name_keys[0]], line):
                match_list = re.findall(dictNames['forename simple'][name_keys[0]], line) # génerer une liste de toute occurence de l'expression recherchée dans la ligne
                for i in range(len(match_list)): # pour autant de fois qu'un résultat de recherche se trouve dans la ligne, basculer sur chaque résultat
                    match = re.search(dictNames['forename simple'][name_keys[0]], line).group(1) # rechercher uniquement la première occurence de l'expression cherchée
                    # la commande .search() renvoie un <re.Match object; span=(116,125), match=' Daniella'>, mais la commande ajoutée à la fin, .group(0), renvoie le groupe premier de cette recherche, donc 'Daniella'
                    line = re.sub(dictNames['forename simple'][name_keys[0]], " {persName}{tag1}{match}{tag2}".format(persName=dictNames['id'][name_keys[1]], tag1='<forename>', match=match, tag2='</forename></persName>'), line, 1)
                    if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"(?:> )"), '>', line)
                    if re.search(re.compile(r"  "), line):
                        line = re.sub(re.compile(r"  "), ' ', line)
    for key in dictNames['forename with honorific']:
        if key == name:
            id = 'id {}'.format(name)
            find_name = name
            name_keys = [find_name, id]
            if re.search(dictNames['forename with honorific'][name_keys[0]], line):
                match_list = re.findall(dictNames['forename with honorific'][name_keys[0]], line) # génerer une liste de toute occurence de l'expression recherchée dans la ligne ; les listes seront des listes de tuple parce que l'expression régulière cherche trois objets : l'expression entière, la première partie et la deuxième
                # ex. [('Médora', '', ''), ('miss Médora', 'miss', 'Médora')]
                for i in range(len(match_list)):
                    if match_list[i][1] == '': # si le tuple trouvé n'a que le prénom sans honorific, donc le deuxième du groupe est vide
                        match = re.search(dictNames['forename with honorific'][name_keys[0]], line) # retrouver la première occurence du mot
                        line = re.sub(dictNames['forename with honorific'][name_keys[0]], " {persName}{tag1}{match}{tag2}".format(persName=dictNames['id'][name_keys[1]], tag1='<forename>', match=match.group(1), tag2='</forename></persName>'), line, 1) # faire la substitution sur le match seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où elle différe
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"(?:> )"), '>', line)
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"  "), ' ', line)
                    else: #
                        match = re.search(dictNames['forename with honorific'][name_keys[0]], line) # retrouver la première occurence du mot
                        line = re.sub(dictNames['forename with honorific'][name_keys[0]], " {persName}{tag1}{honorific}{tag2}{match}{tag3}".format(persName=dictNames['id'][name_keys[1]], tag1='<addName type="honorific">', honorific=match.group(2), tag2='</addName><forename>', match=match.group(3), tag3='</forename></persName>'), line, 1) # faire la substitution sur le match seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où elle différe
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"(?:> )"), '>', line)
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"  "), ' ', line)
    # si le nom entré dans la fonction appartient à un personnage connu par son nom de famille
    for key in dictNames['surname']:
        if key == name:
            id = 'id {}'.format(name)
            find_name = name
            name_keys = [find_name, id]
            if re.search(dictNames['surname'][name_keys[0]], line):
                match_list = re.findall(dictNames['surname'][name_keys[0]], line) # génerer une liste de toute occurence de l'expression recherchée dans la ligne ; les listes seront des listes de tuple parce que l'expression régulière cherche trois objets : l'expression entière, la première partie et la deuxième
                # ex. [('Médora', '', ''), ('miss Médora', 'miss', 'Médora')]
                for i in range(len(match_list)):
                    if match_list[i][1] == '': # si le tuple trouvé n'a que le prénom sans honorific, donc le deuxième du groupe est vide
                        match = re.search(dictNames['surname'][name_keys[0]], line) # retrouver la première occurence du mot
                        line = re.sub(dictNames['surname'][name_keys[0]], " {persName}{tag1}{match}{tag2}".format(persName=dictNames['id'][name_keys[1]], tag1='<surname>', match=match.group(0), tag2='</surname></persName>'), line, 1) # faire la substitution sur le match seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où elle différe
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"(?:> )"), '>', line)
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"  "), ' ', line)
                    else: #
                        match = re.search(dictNames['surname'][name_keys[0]], line) # retrouver la première occurence du mot
                        line = re.sub(dictNames['surname'][name_keys[0]], " {persName}{tag1}{honorific}{tag2}{match}{tag3}".format(persName=dictNames['id'][name_keys[1]], tag1='<addName type="honorific">', honorific=match.group(1), tag2='</addName><surname>', match=match.group(2), tag3='</surname></persName>'), line, 1) # faire la substitution sur le match seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où elle différe
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"(?:> )"), '>', line)
                        if re.search(re.compile(r"  "), line):
                            line = re.sub(re.compile(r"  "), ' ', line)
    # si le nom entré dans la fonction appartient à un personnage connu par son prénom et nom de famille
    for key in dictNames['fullName']:
        if name == key:
            id = 'id {}'.format(name)
            find_name = name
            name_keys = [find_name, id]
            if re.search(dictNames['fullName'][name_keys[0]], line):
                match_list = re.findall(dictNames['fullName'][name_keys[0]], line)
                for i in range(len(match_list)):
                    match = re.findall(dictNames['fullName'][name_keys[0]], line)
                    line = re.sub(dictNames['fullName'][name_keys[0]], ' {persName}{tag1}{forename}{tag2}{tag3}{surname}{tag4}'.format(persName=dictNames['id'][name_keys[1]], tag1='<forename>', forename=match[0][0], tag2='</forename>', tag3='<surname>', surname=match[0][1], tag4='</surname></persName>'), line, 1)
                    if re.search(re.compile(r"  "), line):
                        line = re.sub(re.compile(r"(?:> )"), '>', line)
                    if re.search(re.compile(r"  "), line):
                        line = re.sub(re.compile(r"  "), ' ', line)
    # si le nom entré dans la fonction appartient à un lieu
    for key in dictNames['placeName']:
        if name == key:
            id = 'id {}'.format(name)
            find_name = name
            name_keys = [find_name, id]
            if re.search(dictNames['placeName'][name_keys[0]], line):
                match_list = re.findall(dictNames['placeName'][name_keys[0]], line)
                for i in range(len(match_list)):
                    line = re.sub(dictNames['placeName'][name_keys[0]], ' {tag1}{name}{tag2}'.format(tag1=dictNames['id'][name_keys[1]], name=match_list[0], tag2='</placeName>'), line, 1)
                    if re.search(re.compile(r"  "), line):
                        line = re.sub(re.compile(r"(?:> )"), '>', line)
                    if re.search(re.compile(r"  "), line):
                        line = re.sub(re.compile(r"  "), ' ', line)
    return(line)