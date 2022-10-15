# Real-time-network-multiplayer-game

We have made a multiplayer game.So the rule of the game is that initially the screen will have many squares and the
players have to click on those squares to earn points and the player with maximum points finally wins the game.So,
initially the screen will have many squares, all squares will have their coordinates. The game will have multiple players
and all of them will join the server to play the game.All squares will be at same position in all the players screens. All
players click on join button. After that, the game will start. So the game is to click on the squares. As one player clicks
on the square, that particular square should disappear from screens of all the players and that player will get the point
for that square. Now if there is a delay, meaning if a player clicks a square and another player clicks on the same square
before the square disappears, so this way both players will get the point for the same square. This should not happen.
So, to resolve this every square will have its id and when a player clicks a square, the player’s name along with the time
at which square is clicked will be sent to the server. In this way, if a player clicks the square after a player, then its
points will be rolled back as his timestamp value will be higher than the other player. This way, as all the balls disappear
from the screen, the game will finish and finally the name of the winner will show up on the screen.