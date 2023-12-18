# MAGIC TOURNAMENTS
#### Video Demo: <https://youtu.be/CjM7MVqh5wY>
#### Description:

Magic Tournaments is a web app to create and store magic the gathering tournaments and matches.
Magic the gathering is a famous card game and you can play 1vs1 classic mode with another person or commander mode with 3 or 4 players.
The app allows you to create leagues, tournaments and matches with customized players and decks.

First of all, the app starts with the index.html page where there are two buttons to login.html and register.html pages. In the footer there is also a link to the github repository.
In login.html there are two input fields to enter the username and password. There is also a link to register.html below.
In register.html there are three input fields to enter the username, password and password confirmation. There is also a link to login.html below.

The user can then access to home.html, which is the main page and there are the buttons to navigate to create_l.html, current_l.html and eliminate.html.
In the header there is a menu button that displays in all the followings pages.
With the menu the user can navigate to home.html, eliminate.html, settings.html and log out route.

In eliminate.html the user can delete the active leagues and tournaments.
In settings.html the user can change the username and the password.
And with the log out button the user log out of the session and is redirected to login.html page.

Next, in create_l.html the user can create a league entering the league name, player names and deck names.
Minimum must be entered two player names and deck names. And maximum must be entered four player names and eight deck names.
When form is correctly submited the create button takes the user to current_l.html.

In current_l.html all the user's active leagues are displayed.
For each league there is the league name, player names, deck names, a button to create_t.html and another button to current_t.html.

In create_t.html the user can create a tournament "inside" the league.
There first field is for the tournament name.
Player names and deck names are then displayed with a check box to give the user the option to choose which players and decks are included in the tournament.

When the tournament is successfully created the user is redirected to current_t.html page and there all the league´s active tournaments are displayed.
For each tournament there is the name of the league, the name of the tournament, the names of the selected players with their scores (which starts at zero by default) and the names of the selected decks.
Below there are also two buttons to navigate to create_m.html and current_m.html pages.

In create_m.html page the user can create a match "inside" the tournament. 
All the tournament players are displayed, with a selecting bar that contains the tournament decks, to enter the deck the player have played with the match.
And also a winner check box to indicate what player is the match winner. 
The winning player´s score is updated with plus one.

Next to submit the match the user is redirected to current_m.html where all the tournament matches are shown.
For each match there is the tournament name and the player names with a winner field and their played decks.
And below there is also a trash button to delete.html where you can delete the match.

For the python files, in auth.py there are the login, register and log out routes.
In main.py there all the rest of the routes.
In forms.py there are the Flask forms to validate the data of all templates.
In models.py there are is all the database estructure including Users, Leagues, Players, Decks, Tournaments, Matches and Scores.
In config.py there are some app configurations.
And run.py is the file to run the app.

The requirements.txt includes all the necesary dependencies for the app.

And for the last file, render.yaml, this file includes the hosting (render.com) configurations.




