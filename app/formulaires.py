from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Utilisateur

class FormulaireEtablirSession(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(message="Nom est un champ obligatoire")])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(message="Mot de passe est un champ obligatoire")])
    se_souvenir_de_moi = BooleanField('Se souvenir de moi')
    soummettre = SubmitField('Établir une session')


class FormulaireEnregistrement(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    courriel = StringField('Courriel', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    mot_de_passe2 = PasswordField('Mot de passe (entrer à nouveau)', validators=[DataRequired(), EqualTo('mot_de_passe')])
    soumettre = SubmitField('Enregistrer')

def validate_nom(self, nom):
    utilisateur = Utilisateur.query.filter_by(nom=nom.data).first()
    if utilisateur is not None:
        raise ValidationError('Ce nom existe déjà.')

def validate_courriel(self, courriel):
    utilisateur = Utilisateur.query.filter_by(email=courriel.data).first()
    if utilisateur is not None:
        raise ValidationError('Ce courriel existe déjà.')


class FormulaireEditerProfil(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    a_propos_de_moi = TextAreaField('À propos de moi')
    soumettre = SubmitField('Soumettre')

class FormulaireVide(FlaskForm):
    soumettre = SubmitField('Enregistrer')

class FormulairePublication(FlaskForm):
    publication = TextAreaField('Dite quelque chose...', validators=[DataRequired(), Length(min=1, max=140)])
    soumettre = SubmitField('Soumettre')