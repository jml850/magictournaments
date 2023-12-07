from __init__ import app, db
from models import User, League, Match, Player, Tournament, Deck


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

