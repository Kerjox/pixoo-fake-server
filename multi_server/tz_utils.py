import os
import logging

# Configure logger
logger = logging.getLogger(__name__)

def get_posix_tz_string(tz_name: str) -> str:
    """
    Given a timezone name (e.g., "Europe/Madrid"),
    it searches for the zone file in /usr/share/zoneinfo and extracts the POSIX TZ string,
    which may have the format "CET-1CEST,M3.5.0,M10.5.0/3".
    """
    logger.info(f"Retrieving POSIX TZ string for timezone: {tz_name}")

    # Base path where zone files are located
    base_dir = "/usr/share/zoneinfo"
    tz_path = os.path.join(base_dir, tz_name)

    if not os.path.exists(tz_path):
        logger.error(f"The zone file for {tz_name} was not found in {base_dir}")
        raise ValueError(f"The zone file for {tz_name} was not found in {base_dir}")

    with open(tz_path, "rb") as f:
        data = f.read()

    logger.info(f"Successfully read timezone file: {tz_path}")

    # Zone files (TZif format) contain the POSIX TZ string at the end.
    # Generally, this string is found after the last newline.
    # We split the content by newlines and look for the last non-empty line.
    lines = data.split(b'\n')
    for line in reversed(lines):
        stripped = line.strip()
        if stripped:
            try:
                posix_tz = stripped.decode('ascii')
                logger.info(f"Extracted POSIX TZ string: {posix_tz}")
                return posix_tz
            except UnicodeDecodeError:
                logger.warning("Skipping non-ASCII line in timezone file")
                continue

    logger.error("Could not extract the POSIX TZ string.")
    raise ValueError("Could not extract the POSIX TZ string.")

# Example usage:
if __name__ == '__main__':
    tz_name = "Europe/Madrid"
    try:
        posix_tz_string = get_posix_tz_string(tz_name)
        logger.info(f"The POSIX TZ string for {tz_name} is:\n{posix_tz_string}")
    except Exception as e:
        logger.exception("An error occurred while retrieving the POSIX TZ string.")
