import tkinter as tki
from typing import Callable, Dict, List, Any
import time

BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'slateblue'

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 10,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}


class GameGui:
    _buttons: Dict[str, tki.Button] = {}
    _labels: Dict[str, tki.Label] = {}

    def __init__(self, board: list):
        root = tki.Tk()
        root.title("Boogle Game")
        root.resizable(False, False)
        self.board = board
        self.board_rows = len(board)
        self.board_cols = len(board[0])
        self._main_window = root
        self._outer_frame = tki.Frame(root, bg=REGULAR_COLOR,
                                      highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._upper_frame = tki.Frame(self._outer_frame)
        self._upper_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._create_labels_in_upper_frame()

        self._create_buttons_in_lower_frame()
        self._main_window.bind("<Key>", self._key_pressed)

    def run(self) -> None:
        self._main_window.mainloop()

    def _create_buttons_in_lower_frame(self) -> None:
        for i in range(self.board_cols):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(self.board_rows + 1):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(self.board_rows):
            for j in range(self.board_cols):
                self._make_button('*', i, j)

        self._make_button('Lets Go!', 4, 0, columnspan=1)
        self._make_button('Quit Game', 4, 1, columnspan=1)
        self._make_button('Reset Word', 4, 3, columnspan=1)
        self._make_button('Reset Game', 4, 2, columnspan=1)

    def _create_labels_in_upper_frame(self):
        tki.Grid.columnconfigure(self._upper_frame, 0, weight=1)  # type: ignore
        tki.Grid.columnconfigure(self._upper_frame, 1, weight=1)  # type: ignore
        tki.Grid.columnconfigure(self._upper_frame, 2, weight=1)  # type: ignore
        tki.Grid.rowconfigure(self._upper_frame, 0, weight=1)  # type: ignore

        self._make_labels('time', 0, 1)
        self._make_labels('word', 0, 2)
        self._make_labels('score', 0, 3)

    def _make_labels(self, label_text, row, col, columnspan=1, rowspan=1):
        label = tki.Label(self._upper_frame, font=("Courier", 30),
                          bg=REGULAR_COLOR, width=20, relief="ridge")
        label.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._labels[label_text] = label

    def set_time_display(self, display_text: str) -> None:
        self._labels['time'].configure(text=display_text)

    def set_word_display(self, display_text: str):
        self._labels['word'].configure(text=display_text)

    def set_score_display(self, display_text: str):
        self._labels['score'].configure(text=display_text)

    def set_button_command(self, button_name: str, cmd: Callable[[], None]) -> None:
        self._buttons[button_name].configure(command=cmd)

    def get_button_chars(self) -> List[str]:
        return list(self._buttons.keys())

    def _make_button(self, button_char: str, row: int, col: int,
                     rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        button = tki.Button(self._lower_frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[(row, col)] = button

    def _key_pressed(self, event: Any) -> None:
        """the callback method for when a key is pressed.
        It'll simulate a button press on the right button."""
        if event.char in self._buttons:
            self._simulate_button_press(event.char)
        elif event.keysym == "Return":
            self._simulate_button_press("=")

    def set_button_chars(self):
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                self._buttons[(i, j)].configure(text=self.board[i][j])

    def exit_game(self):
        self._main_window.destroy()

    def _simulate_button_press(self, button_char: str) -> None:
        """make a button light up as if it is pressed,
        and then return to normal"""
        button = self._buttons[button_char]
        button["bg"] = BUTTON_ACTIVE_COLOR

        def return_button_to_normal() -> None:
            # find which widget the mouse is pointing at:
            x, y = self._main_window.winfo_pointerxy()
            widget_under_mouse = self._main_window.winfo_containing(x, y)
            # change color accordingly:
            if widget_under_mouse is button:
                button["bg"] = BUTTON_HOVER_COLOR
            else:
                button["bg"] = REGULAR_COLOR

        button.invoke()  # type: ignore
        button.after(100, func=return_button_to_normal)


    def update_clock(self, t):

        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        self._labels['time'].configure(text=timer)
        if t == 0:
            self._labels['time'].configure(text='00:00')
            return
        self._main_window.after(1000, lambda: self.update_clock(t - 1))

# if __name__ == "__main__":
#     cg = GameGui()
#     cg.set_time_display('time')
#     cg.set_word_display('word')
#     cg.update_clock(180)
#     cg.run()
