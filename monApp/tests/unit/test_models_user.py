from monApp.models import User
from monApp import db

def test_user_fields(client):
    with client.application.app_context():
        user = db.session.get(User, "testuser")
        assert user is not None
        assert user.Login == "testuser"
        assert user.Password == "motdepasse"

def test_load_user(client):
    from monApp.app import login_manager
    with client.application.app_context():
        user = login_manager._user_callback("testuser")
        assert user is not None
        assert user.Login == "testuser"