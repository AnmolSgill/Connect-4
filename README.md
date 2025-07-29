Connect-4  
=========  
CP468 Artificial Intelligence Project

DESCRIPTION  
-----------  
This project implements a multi-agent Connect-4 game using decision-making algorithms:  
- Minimax  
- Alpha-Beta Pruning  
- Expectiminimax  
- Gemini API agent (LLM)

Our implementation offers two modes for running the game:

1. **Command-Line Mode (main.py)**  
   - Run via terminal  
   - Text-based interface  
   - Displays number of nodes visited and pruned (where applicable)  
   - Supports all game modes:  
     • AI vs Human  
     • Human vs Gemini  
     • Gemini vs Agent  
     • Agent vs Agent  

2. **GUI Mode (gui.py)**  
   - Uses Pygame to display the board graphically  
   - Displays win/tie messages and pruned count (where applicable) on game termination  
   - Supports the same set of game modes as above

REQUIREMENTS  
------------  
- Python 3.8 or higher  
- pip packages:  
    - pygame  
    - python-dotenv  
    - google-generativeai  

INSTALLATION  
------------  
1. Open a terminal in the project directory.  
2. Install dependencies:

    pip install pygame python-dotenv google-generativeai

3. Create or edit a `.env` file in the project root with your Gemini API key:

    GEMINI_API_KEY=your_api_key_here

COMPILATION  
-----------  
No compilation is needed. All code is written in Python.

HOW TO RUN  
----------  
You can run either of the following two files:

**1. main.py** (Command Line Mode)  

    python main.py

- Use keyboard input to select the game mode and (if needed) Gemini difficulty.
- Outputs node visit counts and pruning stats in the console.

**2. gui.py** (Graphical Interface Mode)  

    python gui.py

- Use mouse input to select the game mode and difficulty.
- Click on a column to place your piece during human turns.
- On game over, it shows who won and how many branches were pruned (if applicable).

NOTES  
-----  
- Default board size is 6 rows × 7 columns.  
- AI search depth is fixed at 6.  
- Expectiminimax includes random moves every 4 turns to simulate chance nodes.  
- Gemini agent requires internet access and a valid API key.  