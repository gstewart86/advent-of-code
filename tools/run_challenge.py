import subprocess
import typer
from loguru import logger
import importlib
from pathlib import Path

app = typer.Typer()

def get_git_root_path():
    return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()

def setup_logging(log_level):
    log_level = log_level.upper()
    logger.add("debug.log", format="{time} {level} {message}", level=log_level)
    logger.debug(f"Logging initialized at {log_level} level")

@app.command()
def run(day: int = typer.Option(..., "--day", help="The day of the challenge"),
        year: int = typer.Option(2023, "--year", help="The year of the challenge"),
        log_level: str = typer.Option("INFO", "--log-level", help="Logging level")):
    setup_logging(log_level)
    git_root = get_git_root_path()
    logger.debug(f"Git root path: {git_root}")

    day_module_name = f"day{day:02d}"
    try:
        day_module = importlib.import_module(f"{year}.{day_module_name}")
        logger.debug(f"Imported module: {year}.{day_module_name}")
    except ModuleNotFoundError:
        logger.error(f"Module for Year {year}, Day {day:02d} not found.")
        raise typer.Exit(code=1)

    input_path = Path(git_root) / f"{year}/day{day:02d}/puzzle_input.txt"
    logger.debug(f"Input path: {input_path}")
    if not input_path.exists():
        logger.error(f"Input file for Year {year}, Day {day:02d} not found.")
        raise typer.Exit(code=1)

    with open(input_path) as f:
        input_data = f.read()
    logger.debug("Input data read successfully")

    result = day_module.solve(input_data)
    logger.info(f"Result for Year {year}, Day {day:02d}: {result}")

if __name__ == "__main__":
    app()
