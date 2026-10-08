from typing import Dict, List, Optional

_clients: Dict[str, dict] = {}


def reset_clients():
    _clients.clear()


def save_client(client: dict) -> dict:
    _clients[client["name"]] = client
    return client


def list_clients() -> List[dict]:
    return sorted(_clients.values(), key=lambda c: c["name"])


def get_client(name: str) -> Optional[dict]:
    return _clients.get(name)
