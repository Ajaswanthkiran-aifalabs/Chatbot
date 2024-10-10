"""create chatprompt table

Revision ID: 471984bd103e
Revises: 7c996bcfe391
Create Date: 2024-09-20 12:11:29.863690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '471984bd103e'
down_revision: Union[str, None] = '7c996bcfe391'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chatprompt',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=False),
    sa.Column('updated_id', sa.UUID(), nullable=True),
    sa.Column('model_type', sa.Integer(), nullable=True),
    sa.Column('content_type_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('isreversed', sa.Boolean(), nullable=True),
    sa.Column('language_type', sa.Integer(), nullable=False),
    sa.Column('istranslated', sa.Boolean(), nullable=True),
    sa.Column('translated_prompt', sa.String(), nullable=True),
    sa.Column('translated_language_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['content_type_id'], ['contenttype.id'], name="fk_chatprompt_content_type_id_contenttype_id"),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name="fk_chatprompt_created_by_user_id"),
    sa.ForeignKeyConstraint(['language_type'], ['languages.id'], name="fk_chatprompt_language_type_languages_id"),
    sa.ForeignKeyConstraint(['model_type'], ['modeltype.id'], name="fk_chatprompt_model_type_modeltype_id"),
    sa.ForeignKeyConstraint(['translated_language_id'], ['languages.id'], name="fk_chatprompt_translated_language_id_languages_id"),
    sa.PrimaryKeyConstraint('id',name="pk_chatprompt_id")
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chatprompt')
    # ### end Alembic commands ###
