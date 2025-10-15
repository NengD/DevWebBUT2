import pytest
from monApp import app, db
from monApp.models import Auteur, Livre, User

@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()
        # Ajouter un auteur de test
        auteur = Auteur(Nom="Victor Hugo")
        db.session.add(auteur)
        db.session.commit()
        # Ajouter un livre de test
        livre = Livre(Prix=19.99, Titre="Les Misérables", Url="http://exemple.com", Img="img.jpg", auteur_id=auteur.idA)
        db.session.add(livre)
        # Ajouter un user de test
        user1 = User(Login="testuser", Password="motdepasse")
        user2 = User(Login="CDAL", Password="AIGRE")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(testapp):
    return testapp.test_client()