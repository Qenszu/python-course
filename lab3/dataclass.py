from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class AppConfig:
    name: str
    debug: bool

@dataclass(slots=True, frozen=True)
class ServerConfig:
    host: str
    port: int
    timeout: int

@dataclass(slots=True, frozen=True)
class AppConfiguration:
    app: AppConfig
    server: ServerConfig