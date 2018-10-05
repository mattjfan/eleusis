![Eleusis](eleusis_logo_dark.png)

# Overview
**NOTE: This game was initially created as part of the KPCB Engineering Fellows Coding Challenge.**

For this challenge, I chose [Eleusis](https://en.wikipedia.org/wiki/Eleusis_(card_game)), an inductive logic game that mirrors the process of the scientific method. I first read about it in Martin Gardner's article on it from his Mathematical Games column. This implementation was based on John Golden's variant, [Eleusis Express](http://www.logicmazes.com/games/eleusis/express.html).

# Usage
To run, simply extract the file, cd into this directory, and run
```
python eleusis.py
```
or, if python3 is aliased under a different name, like **python3** or **python3.6** use that instead. *Note: This program utilizes new features of python, so your python version must be at least 3.6 or it won't compile*.

# Language Choice & Tooling
I chose python for this project, both as it is a language I'm comfortable in, and it's versatility as a language with both OO and functional features, allowing me to demonstrate a few interesting design choices while still being able to write the code within the constraints of the challenge.

I originally wrote and tested the program on my Windows computer running Python 3.7.0. I've also tested it working on Ubuntu running Python 3.6.6 (through WSL), but it should run fine on any version of **Python 3.6** or higher.

Due to time constraints, and the need to test unix compatibility, most of the testing was done by playtesting. Remaining tests can be found in tests.py.

This project was built entirely with Python 3, built-in libraries, and VS Code.

# Custom Rules
You can create your own rules! Rules are created using the Rule(name, callback) constructor which takes a string describing the rule, and a callback that takes the current `Card`, a `List of Cards` on the Mainline (in order played), all cards played as a `List of Cards` (in order played), and the player's current `Hand`. I've taken the sample rules described by John Golden [here](http://www.logicmazes.com/games/eleusis/express.html) and translated them to this format in **rules.py**. Most of these rules can be written as simple lambda expressions. To add a rule, simply add it to the *rules* list in **rules.py**. 

# Design Choices


# Extra Features
I had a lot of fun making this game. Here's some extra features that I wanted to implement, but ran out of time.
- **Procedurally generated composite rules**: Since python supports HOC, I created and tested some methods for the *Rule* class that allow for the composition of rules (i.e. `merge` and `overlay`). Given the complexity of hands and line configurations, the current `odds` methods that I use to determine how difficult a rule is isn't powerful enough to test all possible combinations, and as such, I lacked a good tool for measuring how 'difficult' (or even impossible) some of these composite rules might be. I could add a better testing method if I were to revisit.

 © 2018 Matt Fan
http://mattfan.me/
