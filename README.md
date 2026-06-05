# ROBOT_NAVIGATION_USING_FINITE_AUTOMATA

## Install Dependency
```
pip install -r requirements.txt
```

## Rules:
- the sequence must begin with START and end with STOP (Stop only accecpt on q2 or q4)
- at least one movement F or B must occur before stop is legal.
- pick must occur before Drop or cannot pick twice without droping first. p is only valid in state q2 or q4. D is only valid in q3.
- at least one complete pick-drop tasks must be completed before STOP. 
- Movement F or B or L or R or ... only allowed when energy > 0. energy start at 5.
- when energy = 0. recharge is needed.
- no immediate F or B. if robots use F, B is not used. 
- No two consecutive identical turns. LL and RR are forbidden.
- the robot must perform at least one counter-clockwise 
loop : (forward -> left)x4

## Main: ✅
- Define the command language alphabet
- create DFA/NFA states
- create transition rules
- handle logic
- Files: shared.py, automata.py, validator.py

## Robot Movement & Grid System: ✅
- build 8 * 8 grid System
- Robot coordinates
- Robot directions: north, south, east and west
- Forward / backward movement
- boundary checking
- Direction rotation logic
- Files: robot.py, grid.py

## Energy & Rule Constraints ✅
- the rules: F = forward, B = backward, L = left...
- Energy system
- Recharge logic
- turn restrictions
- Reverse movement restriction
- Left/right balance tracking
- Detect invalid command patterns
- (Rules: energy = 5, recharge only when energy = 0
    no LL or RR and no FB or BF)
- Files: energy.py and constraints.py

## Pick/Drop & Loop detection ✅
- Pick/drop state
- cannot pick twice
- cannot drop before pick
- at least 2 pick-drop tasks
- detect counter-clockwise loop: F L F L F L F L
- Files: loop_detector.py, tasks.py

## Gui/simulation
- create start button
- before move robot press start (others buttons are hidden)
- when start button press, other buttons shows and start buttons will be hidden
- when you ends the tasks, you can stop (robot ) and start button shows
- Files: main.py, grid.py

shared.py  ←  imported by ALL files above
main.py
  └── grid.py
        ├── validator.py
        │     ├── automata.py
        │     └── constraints.py
        │           ├── energy.py
        │           └── loop_detector.py
        └── simulation.py
              ├── robot.py
              └── tasks.py

