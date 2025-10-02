from typing import Dict


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"].startswith("Welcome")


def test_create_and_get_item(client):
    payload: Dict = {"name": "Book", "price": 12.5}
    r = client.post("/items", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Book"
    item_id = data["id"]

    r2 = client.get(f"/items/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == item_id


def test_filters_and_pagination(client):
    client.post("/items", json={"name": "Laptop", "price": 1000})
    client.post("/items", json={"name": "Lamp", "price": 50})
    client.post("/items", json={"name": "Table", "price": 150})

    r = client.get("/items", params={"name": "la"})
    assert r.status_code == 200
    names = [i["name"] for i in r.json()]
    assert "Laptop" in names and "Lamp" in names

    r2 = client.get("/items", params={"min_price": 100, "max_price": 1000})
    assert r2.status_code == 200
    prices = [i["price"] for i in r2.json()]
    assert all(100 <= p <= 1000 for p in prices)

    r3 = client.get("/items", params={"limit": 2, "offset": 1})
    assert r3.status_code == 200
    assert len(r3.json()) in (1, 2)


def test_update_and_delete_item(client):
    created = client.post("/items", json={"name": "Chair", "price": 30}).json()
    item_id = created["id"]

    r = client.put(f"/items/{item_id}", json={"price": 35})
    assert r.status_code == 200
    assert r.json()["price"] == 35

    r2 = client.delete(f"/items/{item_id}")
    assert r2.status_code == 200
    assert "deleted" in r2.json()["message"]


