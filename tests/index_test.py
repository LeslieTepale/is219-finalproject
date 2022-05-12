def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_open_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data

def test_open_register(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"register" in response.data