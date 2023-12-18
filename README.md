# MAGIC TOURNAMENTS
#### Video Demo: <https://youtu.be/CjM7MVqh5wY>
#### Description:

Magic Tournaments is a web app to create and store magic the gathering tournaments and matches.
Magic the gathering is a card game and you can play 1vs1 classic mode with another person or commander mode with 3 or 4 players.
The app allows you to create leagues, tournaments and matches with customized players and decks.

First of all, the app starts with the index.html page where there are two buttons to login.html and register.html pages. In the footer there is also a link to the github repository.
In login.html there are two input fields to enter the username and password. There is also a link to register.html below.
In register.html there are three input fields to enter the username, password and password confirmation. There is also a link to login.html below.

The user can then access to home.html, which is the main page and there are the buttons to navigate to create_l.html, current_l.html and eliminate.html.
In the header there is a menu button that displays in all the followings pages.
With the menu the user can navigate to home.html, eliminate.html, settings.html and log out route.

Next, in create_l.html the user can create a league entering the league name, player names and deck names.
Minimum must be entered two player names and deck names. And maximum must be entered four player names and eight deck names.
When form is correctly submited the create button takes the user to current_l.html.

In current_l.html all the user's active leagues are displayed.
For each league there is the league name, player names, deck names, a button to create_t.html and another button to current_t.html.

In create_t.html the user can create a tournament "inside" the league.
There first field is for the tournament name.
Player names and deck names are then displayed with a check box to give the user the option to choose which players and decks are included in the tournament.

When the tournament is successfully created the user is redirected to current_t.html page and there all the league´s active tournaments are displayed.
For each tournament there is the name of the tournament, the names of the selected players with their scores (which starts at zero by default) and the names of the selected decks.
Below there are also two buttons to navigate to create_m.html and current_m.html pages.

In create_m.html page the user can create a match "inside" the tournament. 
All the tournament players are displayed, with a selecting bar that contains the tournament decks, to enter the deck the players have played with the match. And also a winner check box to indicate who is the match winner.

