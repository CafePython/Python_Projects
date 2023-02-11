import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command("run")
def main(extension: str, 
        directory: Optional[str] = typer.Argument(None, help="Dossier dans lequel chercher."),
        delete: bool = typer.Option(False, help="Supprime les fichiers trouvés")):
    """
    Affiche les fichier trouvéer avec l'extension donnné
    """

    if directory:
        directory = Path(directory) # convertion du chemin en objet pathlib
    else:
        directory = Path.cwd()      # currrent working directory

    if not directory.exists():
        typer.secho(f"Le dossier '{directory}' n'existe pas.", fg=typer.colors.RED)
        raise typer.Exit()

    temp_files = directory.rglob(f"*.{extension}")                              # rglob permet de chercher dans le dossier et dans les sous-dossiers (récursif) - Attention Generator
    files = [i for i in temp_files]

    if delete :
        nb_files = len(files)
        typer.secho(f"Préparation pour suppresion - {nb_files} fichiers concernés:", bold=True, bg=typer.colors.RED, fg=typer.colors.BRIGHT_WHITE)
        for file in files: #files
            typer.secho(f"Fichier: {file}", fg=typer.colors.RED)
        typer.confirm("Voulez vous vraiment supprimer tous les fichiers trouvés?", abort=True) 
        with typer.progressbar(files) as progress:
            for file in progress:
                file.unlink()
        typer.secho(f"Suppression des {nb_files} fichiers terminé", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Fichier trouvés avec l'extension {extension}:", bg=typer.colors.BLUE, fg=typer.colors.BRIGHT_WHITE)
        for file in files:
            typer.echo(file)

@app.command()
def search(extension:str):
    """
    Recherche et affiche les fichiers avec l'extension données dans le dossier donnés et ses sous dossier.

    Args:
        extension (str): extension du fichier à rechercher
    """
    main(extension=extension, directory=None, delete=False,)

@app.command()
def delete(extension:str):
    """
    Supprime les fichiers avec l'extension données dans le dossier donnés et ses sous dossier.

    Args:
        extension (str): extension du fichier à supprimer
    """
    main(extension=extension, directory=None, delete=True,)

if __name__ == "__main__":
    app()
