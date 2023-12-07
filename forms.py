from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField(validators=[DataRequired(), Length(min=1, max=20)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class LeagueForm(FlaskForm):
    league_name = StringField(validators=[DataRequired()])
    player1 = StringField(validators=[DataRequired()])
    player2 = StringField(validators=[DataRequired()])
    player3 = StringField()
    player4 = StringField()
    deck1 = StringField(validators=[DataRequired()])
    deck2 = StringField(validators=[DataRequired()])
    deck3 = StringField()
    deck4 = StringField()
    deck5 = StringField()
    deck6 = StringField()
    deck7 = StringField()
    deck8 = StringField()
    submit = SubmitField()

class TournamentForm(FlaskForm):
    tournament_name = StringField(validators=[DataRequired()])
    players = StringField()
    decks = StringField()
    submit = SubmitField()

class MatchForm(FlaskForm):
    selectdecks = StringField()
    players = StringField()
    winner = StringField()
    submit = SubmitField()

class EliminateForm(FlaskForm):
    leagues = StringField()
    tournaments = StringField()
    submit = SubmitField()

class ChangeForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField(validators=[DataRequired(), Length(min=1, max=20)])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])