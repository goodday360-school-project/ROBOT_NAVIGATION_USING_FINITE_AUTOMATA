# ROBOT_NAVIGATION_USING_FINITE_AUTOMATA

## Rules:
- the sequence must begin with START and end with STOP (Stop only accecpt on q2 or q4)
- at least one movement F or B must occur before stop is legal.
- pick must occur before Drop or cannot pick twice without droping first. p is only valid in state q2 or q4. D is only valid in q3.
- at least two complete pick-drop tasks must be completed before STOP. 
- Movement F or B or L or R or ... only allowed when energy > 0. energy start at 3.
- when energy = 0. recharge is needed.
- no immediate F or B. if robots use F, B is not used. 
- No two consecutive identical turns. LL and RR are forbidden.
- the sequence must contain at least one counter-clockwise loops pattern: FLFLFLFL at lease once.
- the sequence must never contain: FRFRFRFR.
- the total number of L turns and R turns must not exceed 2. Formally: |count(L) - count(R)| <= 2

## Main:
- Define the command language alphabet
- create DFA/NFA states
- create transition rules
- handle logic
- Files: automata.py, validator.py, , main.py

## Robot Movement & Grid System:
- build 8 * 8 grid System
- Robot coordinates
- Robot directions: north, south, east and west
- Forward / backward movement
- boundary checking
- Direction rotation logic
- Files: robot.py, grid.py

## Energy & Rule Constraints
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

## Pick/Drop & Loop detection
- Pick/drop state
- cannot pick twice
- cannot drop before pick
- al least 2 pick-drop tasks
- detect counter-clockwise loop: F L F L F L F L
- reject clockwise loop: F R F R F R F R
- Files: tasks.py and loop_detector.py

## Gui/simulation
- Build GUI
- Draw 8 * 8 grid
- Show robot movement step-by-step
- display: energy, direction, position, carrying object
- input command interface
- animation/update system
- Files: gui.py, simulation.py