from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_stream_returns_requested_chunks() -> None:
    response = client.get("/stream", params={"message": "demo", "count": 3, "delay_ms": 0})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text.count("event: chunk") == 3
    assert '"index": 3' in response.text
    assert '"done": true' in response.text


def test_stream_validates_count() -> None:
    response = client.get("/stream", params={"count": 0})
    assert response.status_code == 422
