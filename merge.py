import click

@click.group()
def main():
    pass

@main.command()
@click.argument('fichier', type=click.STRING)
@click.argument('page', type=click.STRING)
@click.argument('ref', type=click.STRING)
@click.option('--fichier', help='le nom de fichier à ajouter au texte et le numéro de la page"full_text.txt"')
def add(fichier, page, ref):
    out_file = 'data/in_transcription/full_text.txt'
    with open(out_file, 'r', encoding='utf8') as f:
        out_file_reader = f.readlines()

    in_file = 'data/in_transcription/{}.txt'.format(fichier)
    with open(in_file, 'r', encoding='utf8') as f:
        in_file_reader = f.readlines()

    first_lines = [str('<body>\n'), '<pb n="{pn}" ref="{refr}">\n'.format(pn=page, refr=ref)]

    if len(out_file_reader) < 2:
        out_file_reader.append(str(first_lines[0]))
        out_file_reader.append(str(first_lines[1]))
        for line in in_file_reader:
            out_file_reader.append(line)
        out_file_reader.append('</pb>\n')
        out_file_reader.append('</body>')
    else:
        out_file_reader = out_file_reader[:-1]
        out_file_reader.append(str(first_lines[1]))
        for line in in_file_reader:
            out_file_reader.append(line)
        out_file_reader.append('</pb>\n')
        out_file_reader.append('</body>')

    with open(out_file, 'w', encoding='utf8') as f:
        f.writelines(out_file_reader)

@main.command()
def erase():
    out_file = 'data/full_text.txt'
    with open(out_file, 'w') as f:
        pass

if __name__ == "__main__":
    main()