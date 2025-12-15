# Tank Turmoil

Tank Turmoil is a 1v1 multiplayer tank game where two players battle on a
randomly generated battlefield. Players control tanks using the keyboard
and touchpad, fire multiple weapon types, and collect randomly spawned
power-ups. Walls and boundaries affect movement, while projectiles bounce
off obstacles, creating chaotic and unpredictable gameplay.

Each player has only **one life** — any weapon can hit you, from anywhere,
fired by anyone. Have fun!

## Demo / Gameplay

Instructions on how to play are displayed directly in-game.
No external shortcut commands are required.

## Project Structure

```
Tank-Turmoil_15112-Term-Project/
├── src/
│   ├── Tank wars main program.py
│   ├── tank.py
│   ├── cannon.py
│   ├── clusterCannon.py
│   ├── laser.py
│   ├── mazeGen.py
│   └── segments.py
├── docs/
│   └── 15112 TP Proposal.docx
├── README.md
```

## Dependencies

This project requires the **CMU Graphics** animation package.

Download it from:
https://academy.cs.cmu.edu/desktop

After downloading, place the `cmu_graphics` folder in the project root:

```
Tank-Turmoil_15112-Term-Project/
├── cmu_graphics/
├── src/
├── docs/
└── README.md
```

No other external libraries are required.

## How to Run

Once `cmu_graphics` is installed and placed correctly, run:

```bash
python src/"Tank wars main program.py"
```

## Technical Highlights

- **Recursion & backtracking**
  - Random battlefield generation
  - Laser weapon path generation

- **Geometric collision detection**
  - Cross-product–based dot-rectangle overlap testing
  - Supports collision detection on rotated tank bodies

- **Physics-based interactions**
  - Projectile bouncing off walls
  - Unpredictable weapon trajectories

## Notes

This project was developed as part of **CMU 15-112**.
The `cmu_graphics` package is not included in this repository and must be
installed separately.
