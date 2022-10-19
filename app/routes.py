from flask import render_template, flash, redirect, url_for
from app import app
from app.formulaires import FormulaireEtablirSession
from app.models import Utilisateur
from flask_login import current_user, login_user, logout_user


@app.route('/')
@app.route('/index')
def index():
    Utilisateurs = Utilisateur.query.all()

    return render_template('index.html', titre='Accueil', utilisateurs=Utilisateurs)

    #user = {'username': 'Patate'}
    #posts = [
    #    {
    #        'author': {'username': 'Monsieur Patate'},
    #        'body': 'Vive les Patates !'
    #    },
    #    {
    #        'author': {'username': 'Madame Patate'},
    #        'body': 'Patate !!!'
    #    }
    #]
    return render_template('index.html', title='Accuiel', user=user, posts=posts)

@app.route('/etablir_session', methods=['GET', 'POST'])
def etablir_session():
    if current_user.is_authentificated:
        return redirect(url_for('index'))

    formulaire = FormulaireEtablirSession()
    if formulaire.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(nom=formulaire.nom.data).first()
        if utilisateur is None or not utilisateur.valider_mot_de_passe(formulaire.mot_de_passe.data):
            flash('Nom utilisateur ou mot de passe invalides')
            return redirect(url_for('etablir_session'))
        login_user(utilisateur, remember=formulaire.se_souvenir_de_moi.data)
        return redirect(url_for('index'))
    return render_template('etablir_session.html', title='Établir une session', formulaire=formulaire)