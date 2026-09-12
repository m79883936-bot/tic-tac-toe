from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.metrics import dp
import random


class TicTacToe(App):

    def build(self):
        self.board = [""] * 9
        self.game_over = False
        self.vs_ai = True

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        title = Label(
            text="TIC TAC TOE",
            font_size=dp(30),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )
        root.add_widget(title)

        self.status = Label(
            text="Your Turn  •  X",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(45)
        )
        root.add_widget(self.status)

        self.board_grid = GridLayout(
            cols=3,
            rows=3,
            spacing=dp(5),
            padding=dp(2)
        )

        self.buttons = []

        for i in range(9):
            button = Button(
                text="",
                font_size=dp(50)
            )

            button.bind(
                on_press=lambda btn, i=i:
                self.player_move(i)
            )

            self.buttons.append(button)
            self.board_grid.add_widget(button)

        root.add_widget(self.board_grid)

        new_game = Button(
            text="NEW GAME",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(55)
        )

        new_game.bind(
            on_press=lambda x: self.new_game()
        )

        root.add_widget(new_game)

        self.mode_button = Button(
            text="PLAYER VS AI",
            font_size=dp(18),
            size_hint_y=None,
            height=dp(50)
        )

        self.mode_button.bind(
            on_press=lambda x: self.change_mode()
        )

        root.add_widget(self.mode_button)

        return root

    def player_move(self, i):

        if self.game_over:
            return

        if self.board[i] != "":
            return

        if not self.vs_ai and self.board.count("") < 9:
            symbol = "X" if self.board.count("X") <= self.board.count("O") else "O"
        else:
            symbol = "X"

        self.board[i] = symbol
        self.update_board()

        winner, line = self.check_winner()

        if winner:
            self.finish(winner, line)
            return

        if self.vs_ai:
            self.status.text = "AI Thinking..."
            Clock.schedule_once(lambda dt: self.ai_move(), 0.25)
        else:
            next_player = "O" if symbol == "X" else "X"
            self.status.text = next_player + " Turn"

    def ai_move(self):

        if self.game_over:
            return

        empty = [
            i for i in range(9)
            if self.board[i] == ""
        ]

        if not empty:
            return

        # AI tries to win
        for i in empty:
            self.board[i] = "O"

            if self.check_winner()[0] == "O":
                self.update_board()
                self.finish("O", self.check_winner()[1])
                return

            self.board[i] = ""

        # AI blocks X
        for i in empty:
            self.board[i] = "X"

            if self.check_winner()[0] == "X":
                self.board[i] = "O"
                self.update_board()
                self.status.text = "Your Turn  •  X"
                return

            self.board[i] = ""

        # Center
        if 4 in empty:
            choice = 4

        # Corners
        else:
            corners = [0, 2, 6, 8]
            available = [
                i for i in corners
                if self.board[i] == ""
            ]

            if available:
                choice = random.choice(available)
            else:
                choice = random.choice(empty)

        self.board[choice] = "O"
        self.update_board()

        winner, line = self.check_winner()

        if winner:
            self.finish(winner, line)
        else:
            self.status.text = "Your Turn  •  X"

    def check_winner(self):

        wins = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]

        for a, b, c in wins:
            if (
                self.board[a] != "" and
                self.board[a] == self.board[b] == self.board[c]
            ):
                return self.board[a], (a, b, c)

        if "" not in self.board:
            return "DRAW", None

        return None, None

    def update_board(self):

        for i, button in enumerate(self.buttons):
            button.text = self.board[i]

    def finish(self, winner, line):

        self.game_over = True

        if winner == "X":
            self.status.text = "🎉 X WINS!"

        elif winner == "O":
            self.status.text = "⭕ O WINS!"

        else:
            self.status.text = "🤝 DRAW!"

    def new_game(self):

        self.board = [""] * 9
        self.game_over = False

        for button in self.buttons:
            button.text = ""

        if self.vs_ai:
            self.status.text = "Your Turn  •  X"
        else:
            self.status.text = "X Turn"

    def change_mode(self):

        self.vs_ai = not self.vs_ai

        if self.vs_ai:
            self.mode_button.text = "PLAYER VS AI"
        else:
            self.mode_button.text = "PLAYER VS PLAYER"

        self.new_game()


TicTacToe().run()