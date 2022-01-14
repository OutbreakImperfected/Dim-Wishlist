from tkinter import *
from interpreter import interpret
from updater import update

LOG_LINE_NUM = 0


class MY_GUI:
    def __init__(self, window_name):
        self.window_name = window_name

        # Label
        self.result_text_label = Label(self.window_name, text="Output")
        self.input_text_label = Label(self.window_name, text="Input")

        # Text box
        self.result_text = Text(self.window_name, width=150, height=20)
        self.input_text = Text(self.window_name, width=150, height=20)

        # Button
        self.interpreter_button = Button(self.window_name, text="Interpret", bg="lightblue", width=10,
                                         command=self.process_input)

        self.update_button = Button(self.window_name, text="Update Database", bg="lightblue", width=20,
                                    command=update)

    def set_init_window(self):
        self.window_name.title("Hash to Text")
        self.window_name.geometry('+300+100')

        # Label
        self.input_text_label.grid(row=0, column=0)
        self.result_text_label.grid(row=13, column=0)

        # Text box
        self.input_text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_text.grid(row=14, column=0, rowspan=15, columnspan=10)

        # Button
        self.interpreter_button.grid(row=13, column=1)
        self.update_button.grid(row=13, column=2)

    def process_input(self):
        st = self.input_text.get(1.0, END)

        res = interpret(st)

        self.result_text.delete(1.0, END)
        self.result_text.insert(1.0, res)


def gui_start():
    init_window = Tk()
    main_ui = MY_GUI(init_window)
    main_ui.set_init_window()

    init_window.mainloop()


gui_start()
