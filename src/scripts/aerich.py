import asyncio
from aerich.cli import cli


async def run_aerich_command(args: list[str]):
    """Helper to run Aerich CLI commands safely."""
    try:
        await cli.main(args)
    except SystemExit:
        # Aerich uses typer which raises SystemExit after CLI runs
        pass


def makemigrations():
    asyncio.run(cli.main(["migrate"]))


def migrate():
    asyncio.run(cli.main(["upgrade"]))


def init():
    """Initialize Aerich for a new project."""
    asyncio.run(run_aerich_command(["init", "-t", "src.core.database.TORTOISE_ORM"]))


def mount():
    """Initialize the database (create schema tables)."""
    asyncio.run(run_aerich_command(["init-db"]))
