def test_ready(app):
    response = app.get("/api/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_invalid(app):
    response = app.get("/api/ready/123")
    assert response.status_code == 404
