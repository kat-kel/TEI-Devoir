import click

@click.group()
def main():
    pass

@main.command()
@click.argument('fichier', type=click.STRING)
@click.argument('ref', type=click.STRING)
@click.option('--fichier', help='le nom de fichier à ajouter au texte et le numéro de la page"full_text.txt"')
def add(fichier, ref):
    out_file = 'data/in_transcription/full_text.txt'
    with open(out_file, 'r', encoding='utf8') as f:
        out_file_reader = f.readlines()

    page = str(fichier)[-1]
    facs = '#{}{}'.format(ref, page)
    in_file = 'data/in_transcription/{}.txt'.format(fichier)
    with open(in_file, 'r', encoding='utf8') as f:
        in_file_reader = f.readlines()

    # pour que cette fonction marche bien, il faut commencer avec les premières pages d'une texte transcrite
    # les premières lignes de la première page doivent conformer à ci-dessous :
    #[0] FEUILLETON DE LA PRESSE --> <div>
    #[1] DATE... --> <div>
    #[2] LA DANIELLA --> <div>
    #[3] CHAPITRE --> <div>
    if len(out_file_reader) < 2: # s'il n'y a pas de contenu dans le fichier
        if page == '1':
            out_file_reader.append('<body>\n') # nouvelle ligne 1 crée le <body>
            out_file_reader.append('\t<div><pb n="{pn}" ref="p{refr}" facs="{f}"/>\n'.format(pn=page, refr=ref, f=facs)) # nouvelle ligne 2 d'une première page commence avec un <div>
            out_file_reader.append('\t{}</div>\n'.format(in_file_reader[0][:-1])) # première ligne du texte sans la saut de ligne à la fin, terminée avec un </div>
            for line in in_file_reader[1:3]:
                out_file_reader.append('\t<div>{}</div>\n'.format(line[:-1]))
            for line in in_file_reader[4:]:
                out_file_reader.append('\t\t<p>{}</p>\n'.format(line[:-1]))
            out_file_reader.append('</body>')
        else:
            print('commencez avec la première page transcrite du journal')
    else:
        if page == '1':
            out_file_reader = out_file_reader[:-1]
            out_file_reader.append('\t<div><pb n="{pn}" ref="p{refr}" facs="{f}"/>\n'.format(pn=page, refr=ref, f=facs)) # nouvelle ligne 2 d'une première page commence avec un <div>
            out_file_reader.append('\t{}</div>\n'.format(in_file_reader[0][:-1])) # première ligne du texte sans la saut de ligne à la fin, terminée avec un </div>
            for line in in_file_reader[1:3]:
                out_file_reader.append('\t<div>{}</div>\n'.format(line[:-1]))
            for line in in_file_reader[4:]:
                out_file_reader.append('\t\t<p>{}</p>\n'.format(line[:-1]))
            out_file_reader.append('</body>')
        else:
            out_file_reader = out_file_reader[:-1] # déplacer jusqu'à la fin le </body> sortant de la boucle précedente
            out_file_reader.append('\n\t\t<pb n="{pn}" ref="p{refr}" facs="{f}"/>\n'.format(pn=page, refr=ref, f=facs))
            out_file_reader.append('\t\t<p>{}</p>\n'.format(in_file_reader[0][:-1]))
            for line in in_file_reader[1:]:
                out_file_reader.append('\t\t<p>{}</p>\n'.format(line[:-1]))
            out_file_reader.append('</body>')

    with open(out_file, 'w', encoding='utf8') as f:
        f.writelines(out_file_reader)

@main.command()
def erase():
    out_file = 'data/in_transcription/full_text.txt'
    with open(out_file, 'w') as f:
        pass

if __name__ == "__main__":
    main()