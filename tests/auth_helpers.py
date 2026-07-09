from __future__ import annotations

DEFAULT_PASSWORDS = {
    "admin": "admin123",
    "leader": "leader123",
    "operator": "operator123",
}


def login_headers(client, username: str, password: str | None = None) -> dict[str, str]:
    pwd = password if password is not None else DEFAULT_PASSWORDS.get(username, "test")
    res = client.post("/api/auth/login", json={"username": username, "password": pwd})
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
