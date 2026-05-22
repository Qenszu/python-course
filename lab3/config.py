import argparse
import yaml
from pathlib import Path
from  ConfigSectionIterator import ConfigSectionIterator
from dataclass import *


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

def enum_yaml(data: dict):
    for idx, key in enumerate(data.keys()):
        print(f"[{idx}] {key}")
    print()
    
    for key, newData in data.items():
        if isinstance(newData, dict):
            if not any(isinstance(v, dict) for v in newData.values()):
                print(f"Sekcja '{key}'")
                keys = newData.keys()
                values = newData.values()
                for k, v in zip(keys, values):
                    print(f"|   {k} -> {v}")

def flatten_config(config: dict, prefix: str = "") -> tuple:
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            yield from flatten_config(value, full_key)
        else:
            yield full_key, value


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

    print()
    print()
    enum_yaml(config_data)

    print()
    print()
    gen = flatten_config(config_data)

    first = next(gen)
    print(f"Pierwsza wartość: {first[0]} = {first[1]}")

    for path, value in gen:
        print(f"  {path} = {value}")


    print()
    print()

    iterator = ConfigSectionIterator(config_data)
    app_config = None
    server_config = None


    for section_name, section_data in iterator:
        print(f"Przetwarzam sekcję: {section_name}")

        if section_name == "app":
            app_config = AppConfig(**section_data)
        elif section_name == "server":
            server_config = ServerConfig(**section_data)

    final_config = AppConfiguration(app=app_config, server=server_config)

    print("\nKonfiguracja załadowana:")
    print(f"  {final_config.app}")
    print(f"  {final_config.server}")

main()