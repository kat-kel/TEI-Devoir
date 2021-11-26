import re

# fichier texte
DOC = "data/XMLeScriptorium/19_janvier_1.txt"

# créer une liste vide pour stocker les modificiations RegEx
# afin de documenter nos modifications
modifications = []

bad_apostrophe = re.compile(r"'")
good_apostrophe = "’"
start_paragraph = re.compile(r'\n\n(^.)')
start_p_tag = "<p>"
end_paragraph = re.compile(r'(.)\n\n')
end_p_tag = "</p>"

# ouvrir le fichier texte en mode de lecture
with open(DOC, 'r', encoding='utf8') as f:
    # créer une liste de chaînes (reader) comptante toutes les lignes du fichier texte
    reader = f.readlines()

# créer un nouveau fichier ('test.txt') pour stocker le texte modifié
with open('transcriptions/test.txt', 'w', encoding='utf8') as f:
    # opération .writelines() itérera sur chaque item de la liste de texte de reader
    # et le placera comme une nouvel item dans la liste de l'objet 'writer'
    writer = f.writelines(reader)
    line_count = 0
    # itérer sur chaque item de la liste 'writer', donc chaque ligne de texte
    for line in reader:
        line_count += 1
        # dans chaque ligne, la variable 'matches' prendra un nouveau valeur
        # chaque fois que l'opération .finditer() trouve l'expression régulière cherchée,
        # c'est-à-dire le bad_apostrophe
        matches = bad_apostrophe.finditer(line)
        # à la fin de la liste 'modfiications', ajouter tous les réstulats de 'matches'
        for match in matches:
            modifications.append(['bad_apostrophe', 'line {}'.format(line_count), match])
            change = re.sub(bad_apostrophe, good_apostrophe, line)
            print("line {line} : {change}".format(line=line_count, change=change))

with open('transcriptions/modifications.txt', 'w', encoding='utf8') as f:
    for item in modifications:
        f.write(str(item) + '\n')