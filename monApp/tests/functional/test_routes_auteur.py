from monApp import app

def test_auteurs_liste(client): #client est la fixture définie dans conftest.py
    response = client.get('/auteurs/')
    assert response.status_code == 200
    assert b'Victor Hugo' in response.data

def test_auteur_update_before_login(client):
    response = client.get('/auteurs/1/update/', follow_redirects=True)
    assert b"Login" in response.data # vérifier redirection vers page Login

def login(client, username, password, next_path):
    return client.post( "/login/",data={"Login": username,"Password": password, "next":next_path} ,follow_redirects=True)

def test_auteur_update_after_login(client,testapp):
    with app.app_context():
        # user non connecté
        response=client.get('/auteurs/1/update/', follow_redirects=False)
        # Redirection vers la page de login
        assert response.status_code == 302
        # vérification redirection vers page Login
        assert "/login/?next=%2Fauteurs%2F1%2Fupdate%2F" in response.headers["Location"]
        # simulation connexion user
        response=login(client, "CDAL", "AIGRE", "/auteurs/1/update/")
        # Page update après connexion
        assert response.status_code == 200

        
def test_auteur_view(client):
    response = client.get('/auteurs/1/view/')
    assert response.status_code == 200
    assert b'Victor Hugo' in response.data