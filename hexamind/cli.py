import argparse
from hexamind.utils.utils._env._env import setup_env_file


def main():
    parser = argparse.ArgumentParser(description="Setup .env file")
    parser.add_argument(
        "-d", "--destination", help="Destination directory for .env file"
    )
    args = parser.parse_args()

    setup_env_file(destination_directory=args.destination)


if __name__ == "__main__":
    main()
