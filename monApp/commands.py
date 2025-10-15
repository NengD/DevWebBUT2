import click, logging as lg
from .app import app, db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    # création de toutes les tables
    db.drop_all()
    db.create_all()

    # chargement de notre jeu de données
    import yaml
    with open(filename, 'r') as file:
        lesLivres = yaml.safe_load(file)

    # import des modèles
    from . models import Auteur,Livre
    
    # première passe : création de tous les auteurs
    lesAuteurs = {}
    for livre in lesLivres :
        auteur = livre["author"]
        if auteur not in lesAuteurs :
            objet = Auteur(Nom=auteur)
            db.session.add(objet)
            lesAuteurs[auteur] = objet
    db.session.commit ()

    # deuxième passe : création de tous les livres
    for livre in lesLivres :
        auteur = lesAuteurs[livre["author"]]
        objet = Livre(Prix=livre["price"],
            Titre=livre["title"],
            Url=livre["url"],
            Img=livre["img"],
            auteur_id = auteur.idA)
        db.session.add(objet)
    db.session.commit()
    lg.warning('Database initialized!')

@app.cli. command ()
def syncdb():
    '''Creates all missing tables . '''
    db.create_all()
    lg.warning('Database synchronized!')
    
from .models import User
from hashlib import sha256

def create_user(login, pwd):
    """Crée un utilisateur avec un mot de passe haché et l'ajoute à la base de données."""
    m = sha256()
    m.update(pwd.encode())
    unUser = User(Login=login, Password=m.hexdigest())
    db.session.add(unUser)
    db.session.commit()
    return unUser

@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newuser (login, pwd):
    '''Adds a new user'''
    create_user(login, pwd)
    lg.warning('User ' + login + ' created!')

@app.cli.command()
@click.argument('login')
@click.argument('newpwd')
def newpasswrd (login, newpwd):
    '''Adds a new password'''
    from . models import User
    from hashlib import sha256
    m = sha256()
    m.update(newpwd.encode())
    user = User.query.get(login)
    if user:
        user.Password = m.hexdigest()
        db.session.commit()
        lg.warning('User ' + login + ' updated!')
    else:
        lg.warning('User ' + login + ' not found!')