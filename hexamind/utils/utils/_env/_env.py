import os
import shutil
from pathlib import Path

import pkg_resources


def setup_env_file(destination_directory=None):
    if destination_directory is None:
        destination_directory = Path.cwd()
    else:
        destination_directory = Path(destination_directory)
        destination_directory.mkdir(parents=True, exist_ok=True)

    template_file = pkg_resources.resource_filename(
        __name__, "hexamind/utils/utils/_env/.env.template"
    )
    env_file = destination_directory / ".env"

    if not env_file.exists():
        shutil.copy(template_file, env_file)
        print(f"Created .env file at {env_file}")
    else:
        print(f".env file already exists at {env_file}")
