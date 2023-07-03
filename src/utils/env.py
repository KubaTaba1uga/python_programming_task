# mypy: ignore-errors
# I couldn't find any stubs to this module
from dotenv import load_dotenv


def load_environment_variables():
    load_dotenv()
