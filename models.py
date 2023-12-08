from app import db
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint

#user 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)

    #back_populates relation with user
    leagues = db.relationship('League', back_populates='user', cascade='all, delete-orphan')
    usertournaments = db.relationship('Tournament', back_populates='tournamentsuser')

    #active user
    def is_active(self):
        return self.active
    
    #get user id
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User('{self.username}')"

#league
class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(100), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

    #foreign key for user.id and back_populates relation with user
    user_id = db.Column(db.Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', back_populates='leagues')

    #backref relation with player
    participants = db.relationship('Player', back_populates='league', lazy='dynamic', cascade='all, delete-orphan')
    #backref relation with deck
    decks = db.relationship('Deck', back_populates='related_league', lazy='dynamic', primaryjoin='League.id == Deck.league_id', cascade='all, delete-orphan')
    #back_populates relation with tournament
    tournaments = db.relationship('Tournament', back_populates='league', cascade='all, delete-orphan')

    UniqueConstraint('user_id', 'league_name', name='unique_user_league_name')

#players and decks relation table
player_decks = db.Table(
    'player_decks',
    db.Column('player_id', db.Integer, ForeignKey('player.id')),
    db.Column('deck_id', db.Integer, ForeignKey('deck.id'))
)

#tournament participants relation table
tournament_participants = db.Table(
    'tournament_participants',
    db.Column('tournament_id', db.Integer, ForeignKey('tournament.id'), primary_key=True),
    db.Column('player_id', db.Integer, ForeignKey('player.id'), primary_key=True)
)

#match participants relation table
match_participants = db.Table(
    'match_participants',
    db.Column('match_id', db.Integer, ForeignKey('match.id'), primary_key=True),
    db.Column('player_id', db.Integer, ForeignKey('player.id'), primary_key=True)
)

tournament_decks = db.Table(
    'tournament_decks',
    db.Column('tournament_id', db.Integer, ForeignKey('tournament.id')),
    db.Column('deck_id', db.Integer, ForeignKey('deck.id'))
)

match_decks = db.Table(
    'match_decks',
    db.Column('match_id', db.Integer, ForeignKey('match.id')),
    db.Column('deck_id', db.Integer, ForeignKey('deck.id'))
)

match_winners = db.Table(
    'match_winners',
    db.Column('match_id', db.Integer, ForeignKey('match.id')),
    db.Column('player_id', db.Integer, ForeignKey('player.id'))
)


#player
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100))

    #foreign key for league.id  and back_populates relation with league
    league_id =  db.Column(db.Integer, ForeignKey('league.id', ondelete='CASCADE'))
    league = db.relationship('League', back_populates='participants')

    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'))
    
    #deck relation
    decks = db.relationship('Deck', secondary=player_decks, back_populates='players')
    #tournament relation
    tournaments = db.relationship('Tournament', secondary=tournament_participants, back_populates='participants')
    matches = db.relationship('Match', secondary=match_participants,back_populates='participants')
    winners_id = db.relationship('Match', secondary=match_participants,back_populates='winners')
    scores = db.relationship('PlayerScore', back_populates='player', cascade='all, delete-orphan')
#tournament
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    tournament_name = db.Column(db.String(100), unique=True, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    tournamentsuser = db.relationship('User', back_populates='usertournaments')

    #back_populates relation with player and tournament participants
    participants = db.relationship('Player', secondary=tournament_participants, back_populates='tournaments')
    
    #back_populates relation with deck and tournament decks
    decks = db.relationship('Deck', secondary=tournament_decks, back_populates='tournaments')
    #foreign key for league.id and back_populates relation with league
    league_id =  db.Column(db.Integer, ForeignKey('league.id', ondelete='CASCADE'))
    league = db.relationship('League', back_populates='tournaments')
    
    #back_populates relation with match
    matches = db.relationship('Match', back_populates='tournament', cascade='all, delete-orphan')
    player_scores = db.relationship('PlayerScore', back_populates='tournament', cascade='all, delete-orphan')

    UniqueConstraint('user_id', 'tournament_name', name='unique_user_tournament_name')


#match
class Match(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)
    
    #foreign key for tournament.id and back_populates relation with tournament
    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id', ondelete='CASCADE'))
    tournament = db.relationship('Tournament', back_populates='matches')

    #back_populates relation with player and match participants
    participants = db.relationship('Player', secondary=match_participants, back_populates='matches')
    winners = db.relationship('Player', secondary=match_winners, back_populates='winners_id')
    matchdecks = db.relationship('Deck', secondary=match_decks, back_populates='decksmatch')

#decks
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_name = db.Column(db.String(100))

    league_id = db.Column(db.Integer, ForeignKey('league.id', ondelete='CASCADE'))

    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'))

    tournaments = db.relationship('Tournament', secondary=tournament_decks, back_populates='decks')
    #back_populates relation with player and player decks
    players = db.relationship('Player', secondary=player_decks, back_populates='decks')
    #back_populates relation with league
    related_league = db.relationship('League', back_populates='decks')
    decksmatch = db.relationship('Match', secondary=match_decks, back_populates='matchdecks')


class PlayerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=0)

    player_id = db.Column(db.Integer, ForeignKey('player.id', ondelete='CASCADE'))
    player = db.relationship('Player', back_populates='scores')

    tournament_id = db.Column(db.Integer, ForeignKey('tournament.id', ondelete='CASCADE'))
    tournament = db.relationship('Tournament', back_populates='player_scores')
