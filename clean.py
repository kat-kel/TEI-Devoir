from mypythonlibrary.mylibrary.generalFormatting import basic_clean, xml_elements
from mypythonlibrary.mylibrary.nameFormatting import format_name, make_index

def main():
    """DOCUMENTATION :
	    La fonction 'main' prend un fichier texte et renvoie une version modifiée vers un nouveau chemin, afin de conserver la version originale. Les modifications ont pour but de nettoyer le texte et de le rendre en conformité.

        paramètres :
            fichier == le fichier TXT à formatter

        sortie : un fichier TXT

	    Note : Le texte doit conformer au modèle décrit ci-dessous :
        (1) La transcription doit être déjà traité par deux expressions régulières dans un éditeur de texte :
            Premièrement, pour fusionner des mots divisés à la fin d'une ligne, sélectionner (-)\n et le remplacer avec rien.
            Deuxièment, pour fusionner des phrases qui traversent des lignes, sélectionner (\b|[__]|\,|\;)\n et le remplacer avec $1•
            Mais si le texte d'origine n'a pas d'espaces pour diviser des paragraphes--comme ceux qui sortent de l'eScriptorium--cette méthode se trompera sur les phrases qui commencent une ligne mais pas un nouveau paragraphe. Il faut donc vérifier avec l'image transcrite que les lignes de texte représentent les paragraphes.
        (2) La transcription aura des diacritiques d'une langue latin.
        (2) Les mots en italique doivent être marqués devant et derrière par deux underscores.
            | ... contre-partie de celle que j’ai surprise à la __Réserve__.
        (3) Les expressions dont le mot ou la lettre est corrumpu sont corrigées en plaçant la correction entre crochets []. Le texte envoyé vers cette fonction devrait corriger uniquement les mots et les lettres illisbles, et pas les mauvaises orthographes.
            | — Il n’y a rien là pour la [vue], ...
            # Dans cet exemple ci-dessus, le mot 'vue' devrait être présente dans la phrase mais il n'était pas lisible dans la source.
	    (4) Les expressions dont une coquille est bien lisible dans la source sont suivies par le mot latin [sic].
            | ... huttes de paille, assez vastes pour abriter.[sic]
            # Dans cet exemple ci-dessus, le point suivi par [sic] a été imprimé en erreur, mais cet erreur est conservé dans la transcription envoyé vers cette fonction.
             """
    
    # identifier le chemin du fichier de départ ; ne le modifiez pas ! ce fichier sera ouvert uniquement dans un mode de lecture
    in_file = 'data/in_transcription/full_text.txt'
    # transformer le fichier en un objet itérable, ce qui s'appelle le 'reader' 
    in_file_reader = read_file(in_file)

    # identifier le chemin du fichier où le texte modifié se trouvera
    out_file = 'data/out_transcription/full_text.xml' 
    # préparer le nouveau fichier en supprimant les anciennes modifications s'il y en a dans le fichier, pour qu'il soit vide au début de la fonction
    out_file = empty_version(out_file)

    # nettoyer les lignes de texte et mettre des balises XML ; chaque ligne de texte lue du fichier 'originaĺ'
    formatted_data = []
    for line in in_file_reader:
        line = basic_clean(line)
        line = xml_elements(line)
        names_list = ['Daniella', 'Medora', 'Harriet', 'Lord B', 'Lady B', 'Jean Valreg', 'Frascati', 'Rome', 'Tartaglia']
        for name in names_list:
            line = format_name(name, line)
        formatted_data.append(line)
    with open(out_file, 'w', encoding='utf8') as f:
        f.writelines(formatted_data)

def empty_version(file_path):
    """DOCUMENTATION :
    	La fonction ouvre le fichier où se stockera le nouveau texte et efacer ses contenus s'il y en a."""
    with open(file_path, 'w') as f:
        pass
    return file_path

def read_file(path):
    """DOCUMENTATION :
	    La fonction ouvre un fichier en mode de lecture et transforme chaque ligne du texte en une chaîne de caractères ; chaque ligne devient un item dans une liste qui s'appelle 'reader'.

	    paramètres :
		    path == le chemin de fichier à lire

	    sortie :
		    reader == une liste de chaînes de caractères, itérable."""
    with open(path, 'r', encoding='utf8') as f:
        reader = f.readlines()
        return reader

if __name__ == "__main__":
    main()
