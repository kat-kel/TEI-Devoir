import re

# fichier texte
DOC = "transcriptions/19_janvier_1.txt"

lines = 0


test_pattern = re.compile(r"Daniella")
bad_apostrphe = re.compile(r"'")
good_apostrophe = "’"

with open(DOC, 'r', encoding='utf8') as f:
    reader = f.readlines()
    for line in reader:
        matches = bad_apostrphe.finditer(line)
        for match in matches:
            print(match)