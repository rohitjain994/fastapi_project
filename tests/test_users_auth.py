
def test_register_user(client):
    r = client.post(
        "/users/register",
        json={"email": "user@example.com", "username": "user", "password": "secret123"},
    )
    assert r.status_code == 200
    data = r.json()["user"]
    assert data["email"] == "user@example.com"


def test_me_items_requires_auth(client):
    r = client.get("/users/me/items")
    assert r.status_code == 401

    r2 = client.get("/users/me/items", headers={"Authorization": "Bearer token"})
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)


def test_token(client):
    r = client.post("/token", data={"username": "alice", "password": "pw"})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"


