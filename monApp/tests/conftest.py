import pytest
from monApp import app, db
from monApp.models import Auteur, Livre, User
from hashlib import sha256

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
        m_user1 = sha256()
        m_user1.update("motdepasse".encode())
        m_user2 = sha256()
        m_user2.update("AIGRE".encode())
        user1 = User(Login="testuser", Password=m_user1.hexdigest())
        user2 = User(Login="CDAL", Password=m_user2.hexdigest())
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(testapp):
    return testapp.test_client()