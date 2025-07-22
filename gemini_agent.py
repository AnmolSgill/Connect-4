import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from environment import EMPTY_SPACE
from random import randint

# Load .env file and get the API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiAgent:
    def __init__(self, player_piece, difficulty="hard"):
        self.piece = player_piece
        self.difficulty = difficulty
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found. Make sure you have a .env file with GEMINI_API_KEY set.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

    def choose_move(self, grid):
        prompt = self._format_prompt(grid)
        print("\nPrompt sent to Gemini:\n", prompt)

        try:
            response = self.model.generate_content(prompt)

            if not response.text:
                raise ValueError("Empty Gemini response")

            # Dynamically build regex pattern to match only currently valid columns
            valid_cols = [str(i) for i in range(len(grid[0])) if grid[0][i] == EMPTY_SPACE]
            pattern = r"\b(" + "|".join(valid_cols) + r")\b"
            match = re.search(pattern, response.text)

            if match:
                move = int(match.group(0))
                print(f"Gemini chose column: {move}")
                return move
            else:
                raise ValueError(f"No valid move found in response: {response.text}")

        except Exception as e:
            print("Gemini API failed or invalid response:", e)
            print("Falling back to random valid move.\n")
            return self._fallback_move(grid)


    def _fallback_move(self, grid):
        valid_cols = [col for col in range(len(grid[0])) if grid[0][col] == EMPTY_SPACE]
        move = randint(0, len(valid_cols) - 1) if valid_cols else 0
        print(f"Fallback move (random): Column {move}")
        return move

    def _format_prompt(self, grid):
        difficulty_instruction = {
            "easy": "Pick a random legal column. No strategy needed.",
            "medium": "Try to block the opponent or create 3 in a row.",
            "hard": "Try to win, block the opponent, and look ahead 2+ moves to set up a win."
        }.get(self.difficulty, "Try to win or block the opponent.")

        board_str = "\n".join([" ".join(map(str, row)) for row in grid])
        return (
            f"You are Player {self.piece} in Connect-4.\n"
            f"The current 6x7 board (0 = empty, 1 = Player 1, 2 = Player 2):\n{board_str}\n\n"
            #f"{difficulty_instruction}\n"
            #"ONLY respond with the best column number (0-6) to drop your piece."
        )
