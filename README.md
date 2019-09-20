# Principles of Artificial Intelligence \[Final project\]

In this project there will be a rogue agent that will be controlled by the user, and will also have an opponent which will take steps randomly across the environment. The rogue agent(user) has to reach the goal state before the opponent to win the game. There are certain hurdles across the map as well like mountain, wall, road along with which the user would also be able to pick medicine and strength that has been placed randomly on the map. On the final goal state there will be a boss to which the user has to fight and win the game.

The agent can be controlled by giving directions as North, South, East and West.

## Code

To run the code, use the following command:
```bash
$ python play.py --height 10 --width 10 \
  --num-powerups 2 --num-monsters 1  --num-dynamic-monsters 1\
  --initial-strength 100 \
  --save-dir map1/ \
  --verbose --show-map --map-type emoji
```

If you want to play against a human (having a human player as an agent in addition to the random or your implemented agent), use the `--play-against-human` flag when calling `play.py`.

To implement a new agent, create a new agent class inheriting from the `BaseAgent` class in the `agent.py` file. You just need to implement the `step(...)` function. Take a look at how `RandomAgent` has been implemented. You can also switch to `HumanAgent` to play by hand and see map printouts.

## Requirements
* Python >= 3.6
* Numpy
* Emoji (package: emoji) -- if you want emoji maps


Base code credits: [Erfan Noury](https://github.com/erfannoury)
