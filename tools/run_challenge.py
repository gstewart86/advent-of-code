import typer
from loguru import logger
import importlib
from pathlib import Path

app = typer.Typer()

def setup_logging():
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

@app.command()
def run(day: int = typer.Option(..., "--day", help="The day of the challenge"),
        year: int = typer.Option(2023, "--year", help="The year of the challenge")):
    setup_logging()
    day_module_name = f"day{day:02d}"
    try:
        day_module = importlib.import_module(f"{year}.{day_module_name}")
    except ModuleNotFoundError:
        logger.error(f"Module for Year {year}, Day {day:02d} not found.")
        raise typer.Exit(code=1)

    input_path = Path(f"{year}/day{day:02d}/puzzle_input.txt")
    if not input_path.exists():
        logger.error(f"Input file for Year {year}, Day {day:02d} not found.")
        raise typer.Exit(code=1)

    with open(input_path) as f:
        input_data = f.read()

    result = day_module.solve(input_data)
    logger.info(f"Result for Year {year}, Day {day:02d}: {result}")

if __name__ == "__main__":
    app()
