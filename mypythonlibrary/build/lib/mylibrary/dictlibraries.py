import re

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