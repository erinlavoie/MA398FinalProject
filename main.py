# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# main.py

import tkinter as tk
import displays


class Controller(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.user_listbox = None
        self.user_to_ip = {}
        self.user_to_window = {}

        self.init_window()

        # build the menus
        self.build_menus()

        # build the display
        self.build_display()

        # set the bindings
        self.set_bindings()

        # init sign in
        self.sign_in()

    def init_window(self):
        self.resizable(width=False, height=False)

        # window width, height
        init_dx = 300
        init_dy = 800

        # set up the geometry for the window
        self.geometry("%dx%d+200+50" % (init_dx, init_dy))

        # set the title of the window
        self.title("Messenger")
        self.update_idletasks()

    def build_menus(self):

        # create a new menu
        menu = tk.Menu(self)

        # set the root menu to our menu
        self.config(menu=menu)

        # create a variable to hold the individual menus
        menulist = []

        # create a file menu
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        menulist.append(filemenu)

        menutext = [['Reset RSA Key \u2318-R', 'Quit \u2318-Q', '-']]
        menucmd = [[self.reset_rsa, self.handle_quit]]

        # build the menu elements and callbacks
        for i in range(len(menulist)):
            for j in range(len(menutext[i])):
                if menutext[i][j] != '-':
                    menulist[i].add_command(label=menutext[i][j], command=menucmd[i][j])
                else:
                    menulist[i].add_separator()

    def build_display(self):
        ### Control ###
        # make a control frame on the right
        rightcntlframe = tk.Frame(self)
        rightcntlframe.pack(side=tk.TOP, padx=2, pady=2, fill=tk.BOTH)

        # use a label to set the size of the right panel
        label = tk.Label(rightcntlframe, text="Available Users", width=self.winfo_width())
        label.pack(side=tk.TOP, pady=10)

        scrollbar = tk.Scrollbar(rightcntlframe, orient=tk.VERTICAL)
        self.user_listbox = tk.Listbox(rightcntlframe, yscrollcommand=scrollbar, height=self.winfo_height())

        scrollbar.config(command=self.user_listbox.yview)
        scrollbar.pack(side=tk.RIGHT)

        self.user_listbox.bind('<<ListboxSelect>>', self.handle_selection)
        self.user_listbox.pack(side=tk.TOP, fill=tk.BOTH, pady=3, padx=3)

        return

    def set_bindings(self):
        self.bind('<Command-q>', self.handle_quit)
        self.bind('<Command-r>', self.reset_rsa)
        self.bind('<Command-e>', self.handle_send)
        return

    def handle_selection(self, event=None):
        return

    def sign_in(self, event=None):
        return

    def handle_send(self, event=None):
        return

    def handle_receive(self, event=None):
        return

    def handle_quit(self, event=None):
        self.destroy()

    def reset_rsa(self, event=None):
        return

    def refocus_display(self, event=None):
        return

    def main(self):
        print('Entering main loop')
        self.mainloop()


if __name__=="__main__":
    controller = Controller()
    controller.main()