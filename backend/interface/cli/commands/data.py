import typer

from backend.application.use_cases.common.seed_defaults import SeedDefaultsUseCase

app = typer.Typer(help="Data management commands")


@app.command("seed")
def seed_defaults(
    confirm: bool = typer.Option(
        False,
        "--yes", "-y", 
        help="Skip confirmation prompt"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Seed default data (countries, institutions) - REQUIRES CONFIRMATION
    
    This command populates the database with default countries and institutions
    required for the system to function properly.
    """
    
    try:
        typer.echo("🌱 About to seed default data:")
        typer.echo("   • Default countries (Germany, etc.)")
        typer.echo("   • Default institutions (Bundestag, etc.)")
        typer.echo()
        typer.echo("⚠️  This operation will modify the database!")
        
        if not confirm:
            seed_confirmed = typer.confirm("Are you sure you want to proceed?")
            if not seed_confirmed:
                typer.echo("❌ Seeding cancelled")
                return
        
        # Execute seeding
        typer.echo("🌱 Seeding default data...")
        
        use_case = SeedDefaultsUseCase()
        use_case.execute()
        
        typer.echo("✅ Default data seeded successfully!")
        typer.echo("   • Countries and institutions are now available")
        typer.echo("   • You can now run pipelines and create corpora")
        
    except Exception as e:
        typer.echo(f"❌ Failed to seed default data: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
