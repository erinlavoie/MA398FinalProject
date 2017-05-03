# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# displayapp.py

import tkinter as tk
import dialogs
import socketclasses as nw
import displays


class DisplayApp(tk.Tk):
    def __init__(self):

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
        self.name_to_ip = {}
        self.ip_to_name = {}
        self.conversation_listbox = None
        self.add_button = None

        self.username = ""

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
        self.username = l.name
        self.user = nw.User(self)
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

        self.name_to_ip[box.name] = box.ip
        self.ip_to_name[box.ip] = box.name

        conversation_frame = displays.TextDisplay(self.display_container, self)
        conversation_frame.grid(row=0, column=0, sticky="nsew")

        self.conversation_displays[box.name] = conversation_frame

        self.curr_display = conversation_frame

        self.curr_display.get_input().config(state=tk.NORMAL)
        self.curr_display.get_button().config(command=self.handle_send, state=tk.ACTIVE)

        self.curr_display.tkraise()

        self.curr_contact = box.name

        self.user.contact_new_contact(box.ip)
        self.update_conversation_box([self.curr_contact])

        return

    def new_contact2(self, ip):
        box = dialogs.ContactedBy(self, title="New Contact", ip=ip)

        self.name_to_ip[box.name] = ip
        self.ip_to_name[ip] = box.name

        conversation_frame = displays.TextDisplay(self.display_container, self)
        conversation_frame.grid(row=0, column=0, sticky="nsew")

        self.conversation_displays[box.name] = conversation_frame

        self.curr_display = conversation_frame

        self.curr_display.get_input().config(state=tk.NORMAL)
        self.curr_display.get_button().config(command=self.handle_send, state=tk.ACTIVE)

        self.curr_display.tkraise()

        self.curr_contact = box.name
        self.update_conversation_box([self.curr_contact])

        return

    def reset_rsa(self, event=None):
        self.user.reset_keys()
        return

    def handle_quit(self, event=None):
        self.user.close()
        self.destroy()
        return

    def update_conversation_box(self, contacts):

        for contact in contacts:
            self.conversation_listbox.insert(tk.END, contact)

        self.conversation_listbox.pack()

    def refocus_display(self, event):
        contactname = self.conversation_listbox.get(tk.ACTIVE)
        self.curr_contact = contactname
        self.title(self.curr_contact)

        self.curr_display = self.conversation_displays.get(self.curr_contact)
        self.curr_display.tkraise()

    def handle_send(self, event=None):
        message = self.curr_display.get_input().get("1.0", tk.END)
        self.curr_display.get_input().delete('1.0', tk.END)
        self.curr_display.display_message(self.username, message, 'USER')

        self.user.send_message(self.name_to_ip.get(self.curr_contact), message)

    def display_message(self, message, ip):
        if message != "":
            self.curr_display = self.conversation_displays.get(self.ip_to_name.get(ip))
            self.curr_display.tkraise()
            self.curr_contact = self.ip_to_name.get(ip)

            self.curr_display.display_message(self.curr_contact, message, 'CONTACT')

    def main(self):
        print('Entering main loop')
        self.mainloop()


if __name__ == "__main__":
    dapp = DisplayApp()
    dapp.main()
