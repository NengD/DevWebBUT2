from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, EqualTo, ValidationError

class FormAuteur(FlaskForm):
    idA=HiddenField('idA')
    Nom = StringField ('Nom', validators =[DataRequired()])

class FormLivre(FlaskForm):
    idL=HiddenField('idL')
    Prix = StringField ('Prix', validators =[DataRequired()])

from wtforms import PasswordField
from . models import User
from hashlib import sha256
class LoginForm(FlaskForm):
    Login = StringField ('Identifiant')
    Password = PasswordField ('Mot de passe')
    next = HiddenField()
    def get_authenticated_user (self):
        unUser = User.query.get(self.Login.data)
        if unUser is None:
            return None
        m = sha256 ()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.Password else None

class RegisterForm(FlaskForm):
    Login = StringField('Identifiant', validators=[DataRequired()])
    Password = PasswordField('Mot de passe', validators=[DataRequired()])
    ConfirmPassword = PasswordField(
        'Confirmer le mot de passe',
        validators=[DataRequired(), EqualTo('Password', message='Les mots de passe doivent correspondre.')]
    )

    def validate_Login(self, Login):
        if User.query.filter_by(Login=Login.data).first():
            raise ValidationError('Cet identifiant est déjà pris. Veuillez en choisir un autre.')