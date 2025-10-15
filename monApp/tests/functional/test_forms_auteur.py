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
