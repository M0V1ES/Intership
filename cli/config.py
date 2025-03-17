import base64
import toml

with open("config.toml", "r") as filestr:
    config = toml.load(filestr)


def _get_basic_auth() -> str:
    auth = f"{config['auth']['username']}:{config['auth']['password']}"
    return base64.b64encode(auth.encode()).decode()
