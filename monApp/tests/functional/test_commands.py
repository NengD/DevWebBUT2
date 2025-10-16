from monApp.models import User
from monApp import db
from hashlib import sha256

def test_newuser_command(testapp, caplog):
    """
    Teste la commande 'flask newuser'.
    """
    # Le CliRunner permet d'exécuter des commandes flask
    runner = testapp.test_cli_runner()

    # Invoque la commande 'newuser' avec des arguments
    runner.invoke(args=['newuser', 'cli_user', 'a_password'])

    # Vérifie que le message de succès est bien dans la sortie de la commande
    assert 'User cli_user created!' in caplog.text

    # Vérifie que l'utilisateur a bien été ajouté à la base de données
    with testapp.app_context():
        user = User.query.get('cli_user')
        assert user is not None
        assert user.Login == 'cli_user'
        
        # Vérifie que le mot de passe a été correctement haché
        m = sha256()
        m.update('a_password'.encode())
        assert user.Password == m.hexdigest()

def test_newpasswrd_command(testapp, caplog):
    """
    Teste la commande 'flask newpasswrd' pour un utilisateur existant.
    """
    runner = testapp.test_cli_runner()
    # Invoque la commande pour l'utilisateur 'testuser' créé dans conftest.py
    runner.invoke(args=['newpasswrd', 'testuser', 'new_password_123'])

    assert 'User testuser updated!' in caplog.text

    with testapp.app_context():
        user = User.query.get('testuser')
        m = sha256()
        m.update('new_password_123'.encode())
        assert user.Password == m.hexdigest()
