import pytest
from monApp.models import Livre
from monApp import db

def test_livre_fields(testapp):
    with testapp.app_context():
        livre = db.session.get(Livre, 1)
        assert livre.Titre == "Les Misérables"
        assert livre.Prix == pytest.approx(19.99)
        assert livre.auteur is not None