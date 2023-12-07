from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from __init__ import db
from forms import LeagueForm, TournamentForm, MatchForm
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)

@main.route("/")
#index
@main.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('login'):
            return redirect(url_for('auth.login'))
        
        if request.form.get('register'):
            return redirect(url_for('auth.register'))
        
    return render_template('index.html')
    
#home page 
@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')

#create league
@main.route('/create_l', methods=['GET', 'POST'])
@login_required
def create_l():
    from models import League, Player, Deck
    form = LeagueForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            league_name = form.league_name.data
            existing_league = League.query.filter_by(user=current_user, league_name=league_name, active=True).first()
            if existing_league:
                return render_template('create_l.html', form=form)
            
            new_league = League(league_name=league_name, user=current_user)
            db.session.add(new_league)
            db.session.commit()

            player_names = [form.player1.data, form.player2.data, form.player3.data, form.player4.data]
            for name in player_names:
                if name:
                    player = Player(player_name=name, league=new_league)
                    db.session.add(player)

            deck_names = [form.deck1.data, form.deck2.data, form.deck3.data, form.deck4.data, form.deck5.data, form.deck6.data]
            for name in deck_names:
                if name:
                    deck = Deck(deck_name=name, related_league=new_league)
                    db.session.add(deck)

            db.session.commit()

            return redirect(url_for('main.current_l'))
    
    return render_template('create_l.html', form=form)

#current league
@main.route('/current_l', methods=['GET', 'POST'])
@login_required
def current_l():
    from models import League

    active_leagues = League.query.filter_by(user=current_user, active=True).all()

    return render_template('current_l.html', active_leagues=active_leagues)


#create tournament
@main.route('/create_t', methods=['GET', 'POST'])
@login_required
def create_t():
    from models import League, Tournament, Player, Deck, PlayerScore
    form = TournamentForm()

    league_id = request.args.get('league_id')
    
    league = League.query.filter_by(id=league_id).first()
    players = []
    decks = []

    if league:
        players = Player.query.filter_by(league_id=league.id).all()
        decks = Deck.query.filter_by(league_id=league.id).all()

    if request.method == 'POST':    
        if form.validate_on_submit():
            form.players.data = request.form.getlist('players')
            form.decks.data = request.form.getlist('decks')

            tournament_name = form.tournament_name.data

            existing_tournament = Tournament.query.filter_by(tournamentsuser=current_user, tournament_name=tournament_name, active=True).first()
            if existing_tournament:
                return render_template('create_t.html', league_id=league_id, league=league, form=form, players=players, decks=decks)
            
            selected_players = form.players.data
            selected_decks = form.decks.data
            
            tournament = Tournament(tournament_name=tournament_name, league=league, tournamentsuser=current_user)
            db.session.add(tournament)
            db.session.commit()

            for player_id in selected_players:
                player = Player.query.get(int(player_id))
                tournament.participants.append(player)
                player_score = PlayerScore(player=player, tournament=tournament)
                db.session.add(player_score)

            for deck_id in selected_decks:
                deck = Deck.query.get(int(deck_id))
                tournament.decks.append(deck)

            db.session.commit()

            return redirect(url_for('main.current_t', league_id=league_id))
            
    return render_template('create_t.html', form=form, league=league, players=players, decks=decks)

#current tournament
@main.route('/current_t', methods=['GET', 'POST'])
@login_required
def current_t():
    from models import Tournament, League, PlayerScore
    
    league_id = request.args.get('league_id')
    
    league = League.query.filter_by(id=league_id).first()
    
    tournaments = Tournament.query.filter_by(league=league).all()

    player_scores = PlayerScore.query.all()

    
    if request.method == 'POST':
        tournament_id = request.form.get('tournament_id')

        if tournament_id:
            return redirect(url_for('main.create_m', tournament_id=tournament_id))

    return render_template('current_t.html', league=league, tournaments=tournaments, player_scores=player_scores)

#create match
@main.route('/create_m', methods=['GET', 'POST'])
@login_required
def create_m():
    from models import Tournament, Match, Deck, PlayerScore
    form = MatchForm()

    tournament_id = request.args.get('tournament_id')
    
    tournament = Tournament.query.filter_by(id=tournament_id).first()

    tournament_players = tournament.participants

    tournament_decks = tournament.decks
    
    def check_duplicates(list):
        seen = set()
        for num in list:
            if num in seen:
                return True
            seen.add(num)
        return False
            
    if request.method == 'POST':
        form.selectdecks.data = request.form.getlist('selectdecks')
        selected_decks = form.selectdecks.data
        
        if check_duplicates(selected_decks):
            return redirect(url_for('main.create_m', tournament_id=tournament_id, form=form, tournament=tournament, tournament_players=tournament_players, tournament_decks=tournament_decks))

        form.winner.data = request.form.getlist('winner')
        winners = form.winner.data

        match = Match(tournament=tournament)

        for player in tournament_players:

            if str(player.id) in winners:

                player_score = PlayerScore.query.filter_by(player_id=player.id, tournament_id=tournament.id).first()
                
                if player_score:
                    player_score.score += 1

                match.winners.append(player)

        for deck_id in selected_decks:    
            decks = Deck.query.get(int(deck_id))
            match.matchdecks.append(decks)
    

        db.session.add(match)
        db.session.commit()

        return redirect(url_for('main.current_m', tournament_id=tournament_id))
             
    return render_template('create_m.html', form=form, tournament=tournament, tournament_players=tournament_players, tournament_decks=tournament_decks)

#current tournament matches
@main.route('/current_m', methods=['GET', 'POST'])
@login_required
def current_m():
    from models import Tournament, Match
    
    tournament_id = request.args.get('tournament_id')

    tournament = Tournament.query.filter_by(id=tournament_id, active=True).first()
    
    matches = Match.query.filter_by(tournament=tournament).all()

    
    return render_template('current_m.html', tournament=tournament, matches=matches)


#app settings
@main.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    from models import Match

    match_id = request.args.get('match_id')
    tournament_id = request.args.get('tournament_id')
    
    match = Match.query.filter_by(id=match_id).first()

    if request.method == 'POST':
        db.session.delete(match)
        db.session.commit()
        return redirect(url_for('main.current_m', tournament_id=tournament_id))
            
    return render_template('delete.html', match=match)


@main.route('/eliminate', methods=['GET', 'POST'])
@login_required
def eliminate():
    from models import League, Tournament, Match
    from forms import EliminateForm

    form = EliminateForm()

    leagues = League.query.filter_by(user=current_user, active=True).all()

    tournaments = Tournament.query.filter_by(tournamentsuser=current_user, active=True).all()

    if request.method == 'POST':
        form.leagues.data = request.form.getlist('leagues')
        leagueslist = form.leagues.data

        form.tournaments.data = request.form.getlist('tournaments')
        tournamentslist = form.tournaments.data

        for league in leagues:
            if str(league.id) in leagueslist:
                db.session.delete(league)

        for tournament in tournaments:
            if str(tournament.id) in tournamentslist:
                db.session.delete(tournament)

        db.session.commit()

        return redirect(url_for('main.home'))
                
    return render_template('eliminate.html', form=form, leagues=leagues, tournaments=tournaments)

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    from models import User
    from forms import ChangeForm

    form = ChangeForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_username = form.username.data
            new_password = form.password.data
            hashed_password = generate_password_hash(new_password, method='sha256')

            user = User.query.filter_by(id=current_user.id).first()
            
            user.username = new_username
            user.password = hashed_password

            db.session.commit()

            return redirect(url_for('main.home'))

    return render_template('settings.html', form=form)
