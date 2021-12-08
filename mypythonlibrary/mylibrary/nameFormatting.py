import re
# Un module qui contient un dictionnaire de personnages et de lieux qui appartiennent au roman 'Daniella' par George Sand qui sert à informer la fonction 'format_names(2)'.

# un dictionnaire de personnages et des lieux
dictNames = {
    # personnages connus par leurs prénom ; l'expression régulière doit exclure toute occurence dans une ligne déjà mise entre balises
    'forename simple': {
         # versions possibles : Daniella, Frascatine
        'Daniella': re.compile(r"[^(?:name)>]((?:Daniella)|(?:Frascatine))")
        },
    'forename with honorific': {
        # versions possibles : Médora, Medora, m/Miss Médora, m/Miss Medora
        'Medora': re.compile(r"([^(?:name>)|^(?:honorific>)](?:Médora)|(?:([m|M]iss) (Médora)))"),
        # versions  possibles: Harriet, l/Lady Harriet
        'Harriet': re.compile(r"([^(?:name>)|^(?:honorific>)](?:Harriet)|(?:([l|L]ady) (Harriet)))")
        },
    # personnages connus par leurs nom de famille
    'surname': {
        # versions possibles : l/Lord B***
        'Lord B': re.compile(r"(?:([l|L]ord) (B\*\*\*))"),
        # versions possibles : l/Lady B***
        'Lady B': re.compile(r"(?:([l|L]ady) (B\*\*\*))")
        },
    # personnages connus par leurs prénom et nom de famille
    'fullName': {
        # versions possibles : Jean Valreg
        'Jean Valreg': re.compile(r"(?:(Jean) (Valreg))")
        },
    # lieux
    'placeName': {
        'Frascati': re.compile(r"[^(?:\"Fras\">)](?:Frascati)"),
        'Rome': re.compile(r"[^(?:\"Rom\">)](?:Rome)"),
        'Tartaglia': re.compile(r"[^(?:\"Tart\">)](?:Tartaglia)")
        },
    # les id
    'id' :{
        'id Daniella': '<persName ref="Dan">',
        'id Medora': '<persName ref="Med">',
        'id Harriet': '<persName ref="Har">',
        'id Lord B': '<persName ref="LoB">',
        'id Lady B': '<persName ref="LaB">',
        'id Jean Valreg': '<persName ref="Val">',
        'id Frascati': '<placeName ref="Fra">',
        'id Rome': '<placeName ref="Rom">',
        'id Tartaglia': '<placeName ref="Tar">',}
    }

def format_name(name, line):
    # si le nom passé dans la fonction appartient à un personnage connu par son prénom
    for key in dictNames['forename simple']:
        if key == name:
            keys = [name, 'id {}'.format(name)]
            if re.search(dictNames['forename simple'][keys[0]], line):
                # génerer une liste de toute occurence de l'expression recherchée dans la ligne
                match_list = re.findall(dictNames['forename simple'][keys[0]], line)
                for i in range(len(match_list)): # pour autant de fois qu'un résultat de recherche se trouve dans la ligne, basculer sur chaque résultat
                    line = re.sub(dictNames['forename simple'][keys[0]],\
                        " {persName}{startFore}{match}{endAll}".\
                            format(persName=dictNames['id'][keys[1]], startFore='<forename>', match=match_list[i], endAll='</forename></persName>'),\
                                line, 1) # il faut un espace au début de la substitution parce que l'objet motif prend le caractère juste avant le nom, en chercheant des instances déjà formatées avec la chaîne 'name>'
                    line = re.sub(re.compile(r'(?:forename> )'), 'forename>', line)
    # si le nom passé dans la fonction appartient à un personnage connu par son prénom et un honorific
    for key in dictNames['forename with honorific']:
        if key == name:
            keys = [name, 'id {}'.format(name)]
            if re.search(dictNames['forename with honorific'][keys[0]], line):
                # génerer une liste de toute occurence de l'expression recherchée dans la ligne ; les listes seront des listes de tuple parce que l'expression régulière cherche trois objets : l'expression entière, la première partie et la deuxième
                # ex. [('Médora', '', ''), ('miss Médora', 'miss', 'Médora')]
                match_list = re.findall(dictNames['forename with honorific'][keys[0]], line)
                for i in range(len(match_list)):
                    if match_list[i][1] == '': # si le prénom est trouvé sans honorific, donc le deuxième item du tuple est vide
                        # faire la substitution seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où plusieurs matchs se différent
                        line = re.sub(dictNames['forename with honorific'][keys[0]],\
                            "{persName}{startFore}{match}{endAll}".\
                                format(persName=dictNames['id'][keys[1]], startFore='<forename>', match=match_list[i][0], endAll='</forename></persName>'),\
                                    line, 1)
                        line = re.sub(re.compile(r'(?:forename> )'), 'forename>', line)
                    else: # sinon, le tuple contient le prénom et l'honorific
                        # faire la substitution seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où plusieurs matchs se différent
                        line = re.sub(dictNames['forename with honorific'][keys[0]],\
                            "{persName}{startHon}{honorific}{endHon}{startFore}{match}{endAll}".\
                                format(persName=dictNames['id'][keys[1]], startHon='<addName type="honorific">', honorific=match_list[i][1], endHon='</addName>', startFore='<forename>', match=match_list[i][2], endAll='</forename></persName>'),\
                                    line, 1)

    # si le nom passé dans la fonction appartient à un personnage connu par son nom de famille
    for key in dictNames['surname']:
        if key == name:
            keys = [name, 'id {}'.format(name)]
            if re.search(dictNames['surname'][keys[0]], line):
                # génerer une liste de toute occurence de l'expression recherchée dans la ligne ; les listes seront des listes de tuple parce que l'expression régulière cherche deux objets
                # ex. [('B***', ''), ('lord', 'B***')]
                match_list = re.findall(dictNames['surname'][keys[0]], line)
                for i in range(len(match_list)):
                    if match_list[i][1] == '': # si le tuple trouvé n'a que le nom sans honorific, donc le deuxième du groupe est vide
                        line = re.sub(dictNames['surname'][keys[0]],\
                            "{persName}{startSur}{match}{endAll}".\
                                format(persName=dictNames['id'][keys[1]], startSur='<surname>', match=match_list[i][0], endAll='</surname></persName>'),\
                                    line, 1)
                    else: # sinon, le tuple contient le nom de famille et l'honorific
                        # faire la substitution seulement une fois, puis reprendre la boucle pour trouver la prochaine expression recherchée, dans le cas où plusieurs matchs se différent
                        line = re.sub(dictNames['surname'][keys[0]],\
                            "{persName}{startHon}{honorific}{endHon}{startSur}{match}{endAll}".\
                                format(persName=dictNames['id'][keys[1]], startHon='<addName type="honorific">', honorific=match_list[i][0], endHon='</addName>', startSur='<surname>', match=match_list[i][1], endAll='</surname></persName>'),\
                                    line, 1)

    # si le nom passé dans la fonction appartient à un personnage connu par son prénom et son nom de famille
    for key in dictNames['fullName']:
        if name == key:
            keys = [name, 'id {}'.format(name)]
            if re.search(dictNames['fullName'][keys[0]], line):
                # génerer une liste de toute occurence de l'expression recherchée dans la ligne ; les listes seront des listes de tuple parce que l'expression régulière cherche deux objets qui sont toujours présents
                # ex. [('Jean', 'Valreg')]
                match_list = re.findall(dictNames['fullName'][keys[0]], line)
                for i in range(len(match_list)):
                    line = re.sub(dictNames['fullName'][keys[0]],\
                        '{persName}{startFor}{forename}{endFor}{startSur}{surname}{endAll}'.\
                            format(persName=dictNames['id'][keys[1]], startFor='<forename>', forename=match_list[i][0], endFor='</forename>', startSur='<surname>', surname=match_list[i][1], endAll='</surname></persName>'),\
                                line, 1)

    # si le nom passé dans la fonction appartient à un lieu
    for key in dictNames['placeName']:
        if name == key:
            keys = [name, 'id {}'.format(name)]
            if re.search(dictNames['placeName'][keys[0]], line): # vérifier si la ligne passée dans la fonction format_name() contient le nom de lieu
                # parce qu'il n'y a qu'une seule version du nom d'un lieu, un simple .sub() peut remplacer toute occurence du nom
                match = re.search(dictNames['placeName'][keys[0]], line)
                line = re.sub(dictNames['placeName'][keys[0]],\
                    ' {startPlace}{name}{endPlace}'.\
                        format(startPlace=dictNames['id'][keys[1]], name=match.group(0), endPlace='</placeName>'),\
                            line, 1)
                line = re.sub(re.compile(r'(?:"> )'), '">', line)
    return(line)