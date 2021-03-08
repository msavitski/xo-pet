"""
Data structures, used in project.
You may do changes in tables here, then execute
`alembic revision --message="Your text" --autogenerate`
and alembic would generate new migration for you
in src/db/alembic/versions folder.
"""
import enum

from sqlalchemy import (
    Column, Enum, Integer, MetaData, String, Table, ForeignKey, DateTime
)

# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

# Registry for all tables
metadata = MetaData(naming_convention=convention)

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, nullable=False, unique=True),
    Column('email', String(120), nullable=False, unique=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('password', String(128), nullable=False)
)


class Result(enum.Enum):
    win = 'win'
    lose = 'lose'
    tie = 'tie'


stats_table = Table(
    'stats',
    metadata,
    Column('game_id', String(64), primary_key=True, nullable=False, unique=True),
    Column('user_id', Integer, ForeignKey('users.id', name='fk_user_id')),
    Column('game_result', Enum(Result, name='game_result'), nullable=False),
    Column('start_time', DateTime, nullable=False),
    Column('end_time', DateTime)
)


class Character(enum.Enum):
    X = 'X'
    O = 'O'


instance = Table(
    'game_instance',
    metadata,
    Column('game_id', String(64), ForeignKey('stats.game_id', name='fk_game_id'), primary_key=True, nullable=False),
    Column('move_number', Integer, nullable=False),
    Column('row', Integer, nullable=False),
    Column('column', Integer, nullable=False),
    Column('character', Enum(Character, name='character'), nullable=False)
)
