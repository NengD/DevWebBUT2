from monApp.models import User, Auteur, Livre
from monApp import db
from hashlib import sha256
import yaml

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

def test_loaddb_command(testapp, caplog, tmp_path):
    """
    Teste la commande 'flask loaddb'.
    """
    # 1. Créer un fichier de données YAML temporaire
    data_file = tmp_path / "test_data.yml"
    test_data = [
        {
            "author": "Test Author 1",
            "img": "test1.jpg",
            "price": 10.0,
            "title": "Test Book 1",
            "url": "http://test.com/1"
        },
        {
            "author": "Test Author 1",
            "img": "test2.jpg",
            "price": 12.5,
            "title": "Test Book 2",
            "url": "http://test.com/2"
        }
    ]
    data_file.write_text(yaml.dump(test_data))

    # 2. Exécuter la commande loaddb
    runner = testapp.test_cli_runner()
    runner.invoke(args=['loaddb', str(data_file)])

    # 3. Vérifier les logs
    assert 'Database initialized!' in caplog.text

    # 4. Vérifier le contenu de la base de données
    with testapp.app_context():
        assert Auteur.query.count() == 1
        assert Livre.query.count() == 2
        auteur = Auteur.query.filter_by(Nom="Test Author 1").first()
        assert auteur is not None
        assert len(list(auteur.livres)) == 2
