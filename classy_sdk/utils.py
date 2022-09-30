import base64
from datetime import datetime


def convert_image(filename: str) -> str:
    """Converts image to string.

    Args:
        filename: The name of the image to convert.

    Returns:
        The image converted to serializable string representation.
    """
    with open(filename, "rb") as file:
        converted = base64.b64encode(file.read()).decode()
    return converted


def extract_csv_row(filename: str, row: int) -> str:
    """Extracts a selected line from the csv file.

    Args:
        filename:
            A path to the file.
        row:
            The row number to extract.

    Returns:
        The row from the csv file as a string.
    """
    with open(filename, "r") as file:
        extracted = file.readlines()[row - 1 : row][0].strip("\n")
    return extracted


def join_url(*components: str) -> str:
    """Concatenates multiple url components into one url.

    Args:
        *components:
            Multiple url components.

    Returns:
        A complete url.
    """
    clean = [str(comp).strip("/") for comp in components]
    return "/".join(clean)


def validate_iso_datetime(timepoint: str) -> bool:
    """Validates if a timepoint has the required format.

    It must be set in the ISO8601 format and UTC/Zulu timezone,
    e.g. '2022-01-01T00:00:00.000Z'.

    Args:
        A timepoint to validate.
    Returns:
        An original timepoint, if valid, or raises ValueError.
    """
    try:
        datetime.strptime(timepoint, "%Y-%m-%dT%H:%M:%S.%fZ")
        return timepoint
    except ValueError:
        print("Error: The required format is '2022-01-01T00:00:00.000Z'")
        raise
