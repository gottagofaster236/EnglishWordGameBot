from pathlib import Path
from game_client import GameClient


def main():
    client = GameClient(get_managing_roles())
    client.run(get_token())


def get_token():
    return Path("token.txt").read_text().strip()


def get_managing_roles():
    with open("managing_roles.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


if __name__ == '__main__':
    main()
