from app import app, db
from app.models import User, League, Match, Player, Tournament, Deck


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

