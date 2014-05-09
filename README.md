Solving The Castles of Burgundy
===============================

The goal is to solve the boardgame called [The Castles of Burgundy]. Find the manual in PDF format [here].

There are two broad things that we are interested in:

- For a given game configuration, what is the optimal move;
- For a given playerboard, what is the optimal strategy.

These two items are intentionally vague. When we say "game configuration" we don't specify whether or not we are allowed to know the future outcomes of random dice rolls, or future placements of goods tiles, for example. When we say "strategy", we won't specify whether we mean a bunch of game configuration-dependent rules, or general euristics. All insight about the game should be considered a step in the right direction.


Approach
--------

The first step will be to encode the complete game rules and mechanics in terms of Python classes and functions. When this is done, a game can be simulated from beginning to end. From here there are several options. One of them is to write euristic strategies and play them against each other, and in particular check which ones work better with which boards. Another thing that can be done at this stage is to answer the question: given this configuration, what's the optimal move? This can be done by simply having the engine brute-force all possible moves (although this works in theory, in practice the options tree might be too large and euristics might be necessary to prematurely select out very bad moves)


Organization
------------

Here we describe the organization of the game concepts into classes. The complete list of classes are

- SixSidedTile
- GoodsTile
- Gameboard
- EstateTile
- Estate
- PlayerBoard
- Game
- Player

A crucially important function is Player.findOptions(). When called, this places in Player.options a list of FuncObjs that list all possible actions that a player can take. If we want to take that action we can call FuncObj.call(). findOptions() will check the variable Player.effect to check if the present action is done under some effect (some actions have effects on the following actions, like placing a Dark Green tile will allow you to roll another die). Another crucially important function is the closely related .explore(). This function returns a list of all the final states that can be reached by all possible combinations of actions. This is used as the input of a strategy.

A Game is a turn, phase, nplayers, a Gameboard, a list of the Players.

An EstateTile is a tile which belongs to the PlayerBoard, where buildings can be placed.

The function initializeEstate() returns initializes an Estate. This means it returns a bunch of EstateTiles with the correct die numbers, colors and neighbors. 

[The Castles of Burgundy]:http://boardgamegeek.com/boardgame/84876/the-castles-of-burgundy
[here]:http://aleaspiele.de/Pages/DownloadI/?Delimiter=.&File=Instructions_A14_Die+Burgen+von+Burgund%2FFlag_UK%2FA.Burgund.pdf


