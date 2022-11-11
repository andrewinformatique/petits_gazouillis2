"""test

Revision ID: 1a782dbbf824
Revises: 
Create Date: 2022-10-24 10:49:04.271949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a782dbbf824'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('utilisateur',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('mot_de_passe_hash', sa.String(length=128), nullable=True),
    sa.Column('avatar', sa.Text(length=131072), nullable=True),
    sa.Column('a_propos_de_moi', sa.String(length=140), nullable=True),
    sa.Column('dernier_acces', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_utilisateur_email'), 'utilisateur', ['email'], unique=True)
    op.create_index(op.f('ix_utilisateur_nom'), 'utilisateur', ['nom'], unique=True)
    op.create_table('partisans',
    sa.Column('partisan_id', sa.Integer(), nullable=True),
    sa.Column('utilisateur_qui_est_suivi_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['partisan_id'], ['utilisateur.id'], ),
    sa.ForeignKeyConstraint(['utilisateur_qui_est_suivi_id'], ['utilisateur.id'], )
    )
    op.create_table('publications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('corps', sa.String(length=140), nullable=True),
    sa.Column('horodatages', sa.DateTime(), nullable=True),
    sa.Column('utilisateur_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_publications_horodatages'), 'publications', ['horodatages'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_publications_horodatages'), table_name='publications')
    op.drop_table('publications')
    op.drop_table('partisans')
    op.drop_index(op.f('ix_utilisateur_nom'), table_name='utilisateur')
    op.drop_index(op.f('ix_utilisateur_email'), table_name='utilisateur')
    op.drop_table('utilisateur')
    # ### end Alembic commands ###
