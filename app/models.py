from app import db
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import etablir_session
from datetime import datetime

@etablir_session.user_loader
def load_utilisateur(id):
    return Utilisateur.query.get(int(id))

partisans = db.Table('partisans',
db.Column('partisan_id', db.Integer, db.ForeignKey('utilisateur.id')),
db.Column('utilisateur_qui_est_suivi_id', db.Integer, db.ForeignKey('utilisateur.id'))
)

class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    mot_de_passe_hash= db.Column(db.String(128))
    avatar = db.Column(db.Text(131072), index=False, unique=False) 
    a_propos_de_moi = db.Column(db.String(140))
   
    dernier_acces = db.Column(db.DateTime, default=datetime.utcnow)

    publications = db.relationship('Publications', backref='author', lazy='dynamic')

    les_partisans = db.relationship(
        'Utilisateur', secondary=partisans,
        primaryjoin=(partisans.c.partisan_id == id),
        secondaryjoin=(partisans.c.utilisateur_qui_est_suivi_id == id),
        backref=db.backref('partisans', lazy='dynamic'), lazy='dynamic')

    
    def devenir_partisan(self, utilisateur):
        if not self.est_partisan(utilisateur):
            print("ajouter partisan:{}".format(utilisateur.nom))
            self.les_partisans.append(utilisateur)

    def ne_plus_etre_partisan(self, utilisateur):
        if self.est_partisan(utilisateur):
            print("retirer partisan:{}".format(utilisateur.nom))
            self.les_partisans.remove(utilisateur)

    def est_partisan(self, utilisateur):
        return self.les_partisans.filter(
            partisans.c.utilisateur_qui_est_suivi_id == utilisateur.id).count() > 0

    def liste_publications_dont_je_suis_partisan(self):
        publications_suivies = Publications.query.join(
            partisans, (partisans.c.utilisateur_qui_est_suivi_id == Publications.utilisateur_id)).filter(
                partisans.c.partisan_id == self.id)
        mes_publications = Publications.query.filter_by(utilisateur_id=self.id)

        return mes_publications.union(publications_suivies).order_by(Publications.horodatages.desc())
  
    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)

    def enregistrer_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def valider_mot_de_passe(self, mot__de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot__de_passe)



   

class Publications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corps = db.Column(db.String(140))
    horodatages = db.Column(db.DateTime, index=True, default=datetime.utcnow.ToUniversalTime)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

    def __repr__(self):
        return '<Publications {}>'.format(self.corps)






def get_modele(modele, ligne, racine):
    if modele == "publications":
        id = int(ligne[0])
        corps = ligne[1].strip()
        dateheure = ligne[2].strip()

        horodatage= datetime.strptime(dateheure, '%Y-%m-%d %H:%M:%S.%f')
        u = Utilisateur.query.get(id)

        p = Publications (corps=corps, utilisateur_id=id, horodatages=horodatage, author=u )
        print(p)
        return p   
        
    if modele == "utilisateur":
            nom=ligne[0].strip()
            email=ligne[1].strip()
            mot_de_passe_hash=ligne[2].strip()
            a_propos_de_moi=ligne[3].strip()
            fichier = 'base64/'+nom+'.base64'
            source= os.path.join(racine, fichier)
         
            if os.path.isfile(source):
                with open(source, 'r') as mon_avatar:
                    avatar = mon_avatar.read()
            else:
                avatar= "Pas D??fini"


            u = Utilisateur(nom= nom, email = email,mot_de_passe_hash=mot_de_passe_hash, a_propos_de_moi= a_propos_de_moi, avatar=avatar, dernier_acces=datetime.utcnow())
            u.enregistrer_mot_de_passe(mot_de_passe_hash)
            print(u)
    return u

    return None
