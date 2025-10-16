from monApp.models import Auteur
from monApp import db
from monApp.tests.functional.test_routes_auteur import login

def test_auteur_save_success(client, testapp):
    # Créer un auteur dans la base de données
    with testapp.app_context():
        auteur = Auteur(Nom="Ancien Nom")
        db.session.add(auteur)
        db.session.commit()
        idA = auteur.idA
        # simulation connexion user et soumission du formulaire
        login(client, "CDAL", "AIGRE", "/auteur/save/")
        response = client.post("/auteur/save/",
                            data={"idA": idA, "Nom": "Alexandre Dumas"},
                            follow_redirects=True)
        # Vérifier que la redirection a eu lieu vers /auteurs/<idA>/view/ et que le contenu
        # est correct
        assert response.status_code == 200
        assert f"/auteurs/{idA}/view/" in response.request.path
        assert b"Alexandre Dumas" in response.data  # contenu de la page vue
        # Vérifier que la base a été mise à jour
        with testapp.app_context():
            auteur = Auteur.query.get(idA)
            assert auteur.Nom == "Alexandre Dumas"

def test_auteur_insert_success(client, testapp):
    # simulation connexion user et soumission du formulaire
    login(client, "CDAL", "AIGRE", "/auteur/insert/")
    response = client.post("/auteur/insert/",
                           data={"Nom": "Jules Verne"},
                           follow_redirects=True)
    
    # Vérifier que la redirection a eu lieu et que le contenu est correct
    assert response.status_code == 200
    assert b"Jules Verne" in response.data

    # Vérifier que la base a été mise à jour
    with testapp.app_context():
        # On cherche l'auteur par son nom car on ne connait pas son ID à l'avance
        auteur = Auteur.query.filter_by(Nom="Jules Verne").first()
        assert auteur is not None
        assert f"/auteurs/{auteur.idA}/view/" in response.request.path

def test_auteur_erase_success(client, testapp):
    # Créer un auteur à supprimer dans la base de données
    with testapp.app_context():
        auteur_a_supprimer = Auteur(Nom="Auteur A Effacer")
        db.session.add(auteur_a_supprimer)
        db.session.commit()
        idA = auteur_a_supprimer.idA

    # simulation connexion user et soumission du formulaire de suppression
    login(client, "CDAL", "AIGRE", "/auteur/erase/")
    response = client.post("/auteur/erase/",
                           data={"idA": idA},
                           follow_redirects=True)

    # Vérifier que la redirection a eu lieu vers la liste des auteurs
    assert response.status_code == 200
    assert response.request.path == "/auteurs/"
    assert b"Auteur A Effacer" not in response.data
    # Vérifier que l'auteur a bien été supprimé de la base
    with testapp.app_context():
        auteur = Auteur.query.get(idA)
        assert auteur is None
