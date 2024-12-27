from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI microservice"}

def test_read_item():
    response = client.get("/items/1/soney")
    print(response.status_code)
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "soney"}