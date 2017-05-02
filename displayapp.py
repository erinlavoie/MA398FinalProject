# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# displayapp.py

import tkinter as tk
import dialogs
import socketclasses as nw
import displays


class DisplayApp(tk.Tk):
    def __init__(self, width, height):

        # create root
        tk.Tk.__init__(self)
        self.config(background="#adbdf6")

        # window width, height
        self.initDx = 1000
        self.initDy = 600

        # set up the geometry for the window
        self.geometry("%dx%d+200+50" % (self.initDx, self.initDy))

        # set the title of the window
        self.title("Messenger")

        self.conversation_displays = {}
        self.name_to_user = {}
        self.conversation_listbox = None
        self.add_button = None

        self.user = None
        self.curr_contact = None

        self.curr_display = None
        self.display_container = None


        # build the menus
        self.build_menus()

        # build the controls
        self.build_controls()

        # build the display
        self.build_display()

        # bring the window to the front
        self.curr_display.lift()

        self.sign_in()

        # - do idle events here to get actual canvas size
        self.update_idletasks()

        # now we can ask the size of the canvas
        print(self.winfo_geometry())

        # set up the key bindings
        self.set_bindings()

    def sign_in(self):
        l = dialogs.Login(self, title="Login")

        self.user = nw.User(l.name, self)
        self.name_to_user[l.name] = self.user
        self.add_button.config(state=tk.ACTIVE)

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

        menutext = [['New Contact \u2318-N', 'Reset RSA Key \u2318-R', 'Quit \u2318-Q', '-']]
        menucmd = [[self.new_contact, self.reset_rsa, self.handle_quit]]

        # build the menu elements and callbacks
        for i in range(len(menulist)):
            for j in range(len(menutext[i])):
                if menutext[i][j] != '-':
                    menulist[i].add_command(label=menutext[i][j], command=menucmd[i][j])
                else:
                    menulist[i].add_separator()

    def build_controls(self):

        ### Control ###
        # make a control frame on the right
        rightcntlframe = tk.Frame(self, bg="#baffc9")
        rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        # use a label to set the size of the right panel
        label = tk.Label(rightcntlframe, text="Conversations", width=20)
        label.pack(side=tk.TOP, pady=10)

        scrollbar = tk.Scrollbar(rightcntlframe, orient=tk.VERTICAL)
        self.conversation_listbox = tk.Listbox(rightcntlframe, yscrollcommand=scrollbar.set, height=25)
        self.conversation_listbox.bind('<<ListboxSelect>>', self.refocus_display)

        scrollbar.config(command=self.conversation_listbox.yview)
        scrollbar.pack(side=tk.RIGHT)

        self.conversation_listbox.pack(side=tk.TOP, fill=tk.Y, pady=3, padx=3)
        box = tk.Frame(rightcntlframe)

        self.add_button = tk.Button(box, text="+", width=5, command=self.new_contact, state=tk.DISABLED)
        self.add_button.pack(side=tk.TOP, padx=5, pady=3)
        box.pack(side=tk.RIGHT)

        self.update_conversation_box(self.conversation_displays.values())

        return

    def build_display(self):
        self.display_container = tk.Frame(self)
        self.display_container.pack(side=tk.LEFT, fill=tk.BOTH)
        self.display_container.grid_rowconfigure(0, weight=1)
        self.display_container.grid_columnconfigure(0, weight=1)

        self.curr_display = displays.TextDisplay(self.display_container, self)
        self.curr_display.grid(row=0, column=0, sticky="nsew")

        return

    def set_bindings(self):
        self.bind('<Command-q>', self.handle_quit)
        self.bind('<Command-n>', self.new_contact)
        self.bind('<Command-r>', self.reset_rsa)
        self.bind('<Command-e>', self.handle_send)
        return

    def new_contact(self, event=None):
        box = dialogs.NewContact(self, title="New Contact")
        contact = nw.User(self, dst_server_name=box.ip)
        self.name_to_user[box.name] = contact

        conversation_frame = displays.TextDisplay(self.display_container, self)
        conversation_frame.grid(row=0, column=0, sticky="nsew")

        self.conversation_displays[box.name] = conversation_frame

        self.curr_display = conversation_frame

        self.curr_display.get_input().config(state=tk.NORMAL)
        self.curr_display.get_button().config(command=self.handle_send, state=tk.ACTIVE)

        self.curr_display.tkraise()

        self.curr_contact = contact

        return

    def reset_rsa(self, event=None):
        self.user.refresh_keys()
        return

    def handle_quit(self, event=None):
        self.destroy()
        return

    def update_conversation_box(self, contacts):

        for contact in contacts:
            self.conversation_listbox.insert(tk.END, contact.get_username())

        self.conversation_listbox.pack()

    def refocus_display(self, event):
        w = event.widget
        contactname = w.get(int(w.curselection()[0]))
        conversation_display = self.conversation_displays.get(contactname)
        self.curr_display = conversation_display
        self.curr_display.tkraise()

        self.curr_contact = self.name_to_user.get(contactname)

    def handle_send(self, event=None):
        message = self.curr_display.get_input().get("1.0", tk.END)
        self.curr_display.get_input().delete('1.0', tk.END)
        self.curr_display.display_message(self.user.get_username(), message, 'USER1')

        self.curr_contact.set_message(message)

    def handle_receive(self, contact, message):
        if message != "":
            self.curr_display = self.conversation_displays.get(contact.get_username())
            self.curr_display.tkraise()
            self.curr_contact = contact

            self.curr_display.display_message(self.curr_contact.get_username(), message, 'USER2')

    def main(self):
        print('Entering main loop')
        self.mainloop()


if __name__ == "__main__":
    dapp = DisplayApp(1000, 600)
    dapp.main()
