import typer

from backend.interface.cli.commands import pipeline, corpora, data, fetch, extract, preprocess, model

app = typer.Typer(help="Cicero CLI")

# Add sub-commands
app.add_typer(pipeline.app, name="pipeline", help="Pipeline orchestration commands")
app.add_typer(corpora.app, name="corpora", help="Corpora management commands")
app.add_typer(data.app, name="data", help="Data management commands")
app.add_typer(fetch.app, name="fetch", help="Data fetching commands")
app.add_typer(extract.app, name="extract", help="Speech extraction commands")
app.add_typer(preprocess.app, name="preprocess", help="Text preprocessing commands")
app.add_typer(model.app, name="model", help="Modeling and analysis commands")

if __name__ == "__main__":
    app()
