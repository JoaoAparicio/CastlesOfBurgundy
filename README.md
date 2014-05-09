Solving The Castles of Burgundy
===============================

The goal is to solve the boardgame called [The Castles of Burgundy]. Find the manual in PDF format [here].

There are two main goals that we are interested in:

- For a given game configuration, what is the optimal move;
- For a given playerboard, what is the optimal strategy.

Approach
--------

The first step will be to encode the complete game rules and mechanics in terms of Python classes and functions. When this is done, a game can be simulated from beginning to end. From here there are several options. One of them is to write heuristic strategies and play them against each other, and in particular check which ones work better with which boards. Another thing that can be done at this stage is to answer the question: given this configuration, what's the optimal move? This can be done by simply having the engine brute-force all possible moves (although this works in theory, in practice the options tree might be too large and heuristics might be necessary to prematurely select out very bad moves).

Philosophy
----------

The two main goals stated before are intentionally vague. When we say "game configuration" we don't specify whether or not we are allowed to know the future outcomes of random dice rolls, or future placements of goods tiles, for example. When we say "strategy", we won't specify whether we mean a bunch of game configuration-dependent rules, or general heuristics. The key here is the expectation that the solutions to these questions should arrive more or less together. In any case, any insight about the game should be considered a step in the right direction.

Organization
------------

Here we describe the organization of the game concepts into classes. The complete list of classes is

- SixSidedTile
- GoodsTile
- Gameboard
- EstateTile
- Estate
- PlayerBoard
- Game
- Player

A crucially important function is Player.findOptions(). When called, this places in Player.options a list of FuncObjs that list all possible actions that a player can take. If we want to take that action we can call FuncObj.call(). findOptions() will check the variable Player.effect to check if the present action is done under some effect (some actions have effects on the following actions, like placing a Dark Green tile will give you an extra die of your chosing). Another crucially important function is the closely related .explore(). This function returns a list of all the final states that can be reached by all possible combinations of actions.

A 'strategy' is a function that from the complete list of final states that could be attained in a given round by a given player, selects one of those states and sequantially executes the actions that lead to this state. Once all the game mechanics is encoded in this project, one of the things that will become possible is to attribute a certain strategy to a certain player with a certain playerboard, and a different strategy to a different player with a differen playerboard, and see how that plays out. At that point, the crafting of strategies could become its own spin-off project. Reaching this point will effectively separate the two goals into two different projects.

An Estate is a bunch of EstateTiles with the correct die numbers, colors and neighbors. An EstateTile is a tile which belongs to the PlayerBoard, where buildings can be placed. The function initializeEstate() returns initializes an Estate. Different initial playerboards can differ only in their Estate.

[The Castles of Burgundy]:http://boardgamegeek.com/boardgame/84876/the-castles-of-burgundy
[here]:http://aleaspiele.de/Pages/DownloadI/?Delimiter=.&File=Instructions_A14_Die+Burgen+von+Burgund%2FFlag_UK%2FA.Burgund.pdf


