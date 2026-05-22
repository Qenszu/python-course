import argparse
import yaml
from pathlib import Path


REQUIRED_KEYS = [
    "app.name",
    "app.debug",
    "server.host",
    "server.port",
    "database.credentials.user",
    "database.credentials.password",
]


def check_key(data: dict, path: str) -> bool:
    keys = path.split(".")
    node = data
    for key in keys:
        if not isinstance(node, dict) or key not in node:
            return False
        node = node[key]
    return True


def validate_config(data: dict) -> list[str]:
    return [path for path in REQUIRED_KEYS if not check_key(data, path)]


def print_yaml(data: dict, space: str = "") -> None:
    for key, value in data.items():
        print(f"{space}{key}: ", end="")
        if isinstance(value, dict):
            print()
            print_yaml(value, space + "  ")
        else:
            print(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wczytywanie konfiguracji YAML")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Ścieżka do pliku konfiguracyjnego YAML",
    )
    args = parser.parse_args()
    config_path: Path = args.config

    if not config_path.exists():
        print(f"Błąd: plik '{config_path}' nie istnieje.")
        return

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = yaml.load(file, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        print(f"Błąd parsowania YAML: {e}")
        return
    except OSError as e:
        print(f"Błąd odczytu pliku: {e}")
        return

    if not isinstance(config_data, dict):
        print("Błąd: plik YAML nie zawiera słownika na najwyższym poziomie.")
        return

    print_yaml(config_data)
    print()

    missing = validate_config(config_data)
    if missing:
        for path in missing:
            print(f"Brak klucza: {path}")
    else:
        print("Konfiguracja jest poprawna.")


main()