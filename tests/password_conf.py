from app import auth

def check_password(client):
    #response = check_password(auth)
    response = client.get("/dashboard")
    with auth.loginform():
        assert response.status_code == 200