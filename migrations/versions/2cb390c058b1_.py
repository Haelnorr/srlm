"""empty message

Revision ID: 2cb390c058b1
Revises: f695d4e01552
Create Date: 2024-03-23 19:38:56.690073

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2cb390c058b1'
down_revision = 'f695d4e01552'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('division', schema=None) as batch_op:
        batch_op.add_column(sa.Column('league_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('division_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'league', ['league_id'], ['id'])
        batch_op.drop_column('league')

    with op.batch_alter_table('final', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_division_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('home_team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('away_team_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('final_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('final_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('final_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'season_division', ['season_division_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['home_team_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['away_team_id'], ['id'])
        batch_op.drop_column('away_team')
        batch_op.drop_column('season_division')
        batch_op.drop_column('home_team')

    with op.batch_alter_table('final_results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('final_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('winner_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('loser_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('final_results_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('final_results_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('final_results_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'team', ['winner_id'], ['id'])
        batch_op.create_foreign_key(None, 'final', ['final_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['loser_id'], ['id'])
        batch_op.drop_column('final')
        batch_op.drop_column('winner')
        batch_op.drop_column('loser')

    with op.batch_alter_table('lobby', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('lobby_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'match', ['match_id'], ['id'])
        batch_op.drop_column('match')

    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_division_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('home_team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('away_team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('streamer_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('final_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('match_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('match_ibfk_4', type_='foreignkey')
        batch_op.drop_constraint('match_ibfk_5', type_='foreignkey')
        batch_op.drop_constraint('match_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('match_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'team', ['away_team_id'], ['id'])
        batch_op.create_foreign_key(None, 'final', ['final_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['streamer_id'], ['id'])
        batch_op.create_foreign_key(None, 'season_division', ['season_division_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['home_team_id'], ['id'])
        batch_op.drop_column('home_team')
        batch_op.drop_column('away_team')
        batch_op.drop_column('season_division')
        batch_op.drop_column('streamer')
        batch_op.drop_column('final')

    with op.batch_alter_table('match_availability', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('team_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('match_availability_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('match_availability_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'team', ['team_id'], ['id'])
        batch_op.create_foreign_key(None, 'match', ['match_id'], ['id'])
        batch_op.drop_column('team')
        batch_op.drop_column('match')

    with op.batch_alter_table('match_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lobby_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('match_data_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'lobby', ['lobby_id'], ['id'])
        batch_op.drop_column('lobby')

    with op.batch_alter_table('match_result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('winner_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('loser_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('match_result_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('match_result_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'team', ['winner_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['loser_id'], ['id'])
        batch_op.drop_column('winner')
        batch_op.drop_column('loser')

    with op.batch_alter_table('match_schedule', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('match_schedule_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'match', ['match_id'], ['id'])
        batch_op.drop_column('match')

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('first_season_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('player_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('player_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'season_division', ['first_season_id'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_column('first_season')
        batch_op.drop_column('user')

    with op.batch_alter_table('player_award', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('award_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('season_division_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('player_award_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('player_award_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('player_award_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'award', ['award_id'], ['id'])
        batch_op.create_foreign_key(None, 'player', ['player_id'], ['id'])
        batch_op.create_foreign_key(None, 'season_division', ['season_division_id'], ['id'])
        batch_op.drop_column('season_division')
        batch_op.drop_column('award')
        batch_op.drop_column('player')

    with op.batch_alter_table('player_match_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('player_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('team_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('player_match_data_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('player_match_data_ibfk_2', type_='foreignkey')
        batch_op.drop_constraint('player_match_data_ibfk_4', type_='foreignkey')
        batch_op.create_foreign_key(None, 'match_data', ['match_id'], ['id'])
        batch_op.create_foreign_key(None, 'player', ['player_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['team_id'], ['id'])
        batch_op.drop_column('team')
        batch_op.drop_column('player')
        batch_op.drop_column('match')

    with op.batch_alter_table('season', schema=None) as batch_op:
        batch_op.add_column(sa.Column('league_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('season_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'league', ['league_id'], ['id'])
        batch_op.drop_column('league')

    with op.batch_alter_table('team_award', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('award_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('season_division_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('team_award_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('team_award_ibfk_3', type_='foreignkey')
        batch_op.drop_constraint('team_award_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'season_division', ['season_division_id'], ['id'])
        batch_op.create_foreign_key(None, 'award', ['award_id'], ['id'])
        batch_op.create_foreign_key(None, 'team', ['team_id'], ['id'])
        batch_op.drop_column('team')
        batch_op.drop_column('award')
        batch_op.drop_column('season_division')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team_award', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_division', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('award', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('team_award_ibfk_2', 'season_division', ['season_division'], ['id'])
        batch_op.create_foreign_key('team_award_ibfk_3', 'team', ['team'], ['id'])
        batch_op.create_foreign_key('team_award_ibfk_1', 'award', ['award'], ['id'])
        batch_op.drop_column('season_division_id')
        batch_op.drop_column('award_id')
        batch_op.drop_column('team_id')

    with op.batch_alter_table('season', schema=None) as batch_op:
        batch_op.add_column(sa.Column('league', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('season_ibfk_1', 'league', ['league'], ['id'])
        batch_op.drop_column('league_id')

    with op.batch_alter_table('player_match_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('player', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('player_match_data_ibfk_4', 'team', ['team'], ['id'])
        batch_op.create_foreign_key('player_match_data_ibfk_2', 'player', ['player'], ['id'])
        batch_op.create_foreign_key('player_match_data_ibfk_1', 'match_data', ['match'], ['id'])
        batch_op.drop_column('team_id')
        batch_op.drop_column('player_id')
        batch_op.drop_column('match_id')

    with op.batch_alter_table('player_award', schema=None) as batch_op:
        batch_op.add_column(sa.Column('player', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('award', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('season_division', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('player_award_ibfk_3', 'season_division', ['season_division'], ['id'])
        batch_op.create_foreign_key('player_award_ibfk_1', 'award', ['award'], ['id'])
        batch_op.create_foreign_key('player_award_ibfk_2', 'player', ['player'], ['id'])
        batch_op.drop_column('season_division_id')
        batch_op.drop_column('award_id')
        batch_op.drop_column('player_id')

    with op.batch_alter_table('player', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('first_season', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('player_ibfk_1', 'season_division', ['first_season'], ['id'])
        batch_op.create_foreign_key('player_ibfk_2', 'user', ['user'], ['id'])
        batch_op.drop_column('first_season_id')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('match_schedule', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('match_schedule_ibfk_1', 'match', ['match'], ['id'])
        batch_op.drop_column('match_id')

    with op.batch_alter_table('match_result', schema=None) as batch_op:
        batch_op.add_column(sa.Column('loser', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('winner', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('match_result_ibfk_3', 'team', ['winner'], ['id'])
        batch_op.create_foreign_key('match_result_ibfk_2', 'team', ['loser'], ['id'])
        batch_op.drop_column('loser_id')
        batch_op.drop_column('winner_id')

    with op.batch_alter_table('match_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lobby', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('match_data_ibfk_1', 'lobby', ['lobby'], ['id'])
        batch_op.drop_column('lobby_id')

    with op.batch_alter_table('match_availability', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('match_availability_ibfk_1', 'match', ['match'], ['id'])
        batch_op.create_foreign_key('match_availability_ibfk_2', 'team', ['team'], ['id'])
        batch_op.drop_column('team_id')
        batch_op.drop_column('match_id')

    with op.batch_alter_table('match', schema=None) as batch_op:
        batch_op.add_column(sa.Column('final', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('streamer', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('season_division', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('away_team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('home_team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('match_ibfk_2', 'final', ['final'], ['id'])
        batch_op.create_foreign_key('match_ibfk_1', 'team', ['away_team'], ['id'])
        batch_op.create_foreign_key('match_ibfk_5', 'user', ['streamer'], ['id'])
        batch_op.create_foreign_key('match_ibfk_4', 'season_division', ['season_division'], ['id'])
        batch_op.create_foreign_key('match_ibfk_3', 'team', ['home_team'], ['id'])
        batch_op.drop_column('final_id')
        batch_op.drop_column('streamer_id')
        batch_op.drop_column('away_team_id')
        batch_op.drop_column('home_team_id')
        batch_op.drop_column('season_division_id')

    with op.batch_alter_table('lobby', schema=None) as batch_op:
        batch_op.add_column(sa.Column('match', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('lobby_ibfk_1', 'match', ['match'], ['id'])
        batch_op.drop_column('match_id')

    with op.batch_alter_table('final_results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('loser', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('winner', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('final', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('final_results_ibfk_2', 'team', ['loser'], ['id'])
        batch_op.create_foreign_key('final_results_ibfk_3', 'team', ['winner'], ['id'])
        batch_op.create_foreign_key('final_results_ibfk_1', 'final', ['final'], ['id'])
        batch_op.drop_column('loser_id')
        batch_op.drop_column('winner_id')
        batch_op.drop_column('final_id')

    with op.batch_alter_table('final', schema=None) as batch_op:
        batch_op.add_column(sa.Column('home_team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('season_division', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('away_team', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('final_ibfk_3', 'season_division', ['season_division'], ['id'])
        batch_op.create_foreign_key('final_ibfk_2', 'team', ['home_team'], ['id'])
        batch_op.create_foreign_key('final_ibfk_1', 'team', ['away_team'], ['id'])
        batch_op.drop_column('away_team_id')
        batch_op.drop_column('home_team_id')
        batch_op.drop_column('season_division_id')

    with op.batch_alter_table('division', schema=None) as batch_op:
        batch_op.add_column(sa.Column('league', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('division_ibfk_1', 'league', ['league'], ['id'])
        batch_op.drop_column('league_id')

    # ### end Alembic commands ###
