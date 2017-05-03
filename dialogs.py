# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# dialogs.py

import tkinter as tk

class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None, grab = True):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if grab:
            self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+75,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        return 1 # override

    def apply(self):

        pass # override


class NewContact(Dialog):

    def __init__(self, parent, title=None):
        self.e1 = None
        self.e2 = None
        self.ip = None
        self.name = ""
        Dialog.__init__(self, parent, title)

    def body(self, master):

        tk.Label(master, text="Contact IP Address: ").grid(row=0)

        self.e1 = tk.Entry(master)
        self.e1.grid(row=0, column=1)

        tk.Label(master, text="Contact Name: ").grid(row=1)

        self.e2 = tk.Entry(master)
        self.e2.grid(row=1, column=1)

    def apply(self):
        self.ip = self.e1.get()
        self.name = self.e2.get()

        return self.ip

class ContactedBy(Dialog):

    def __init__(self, parent, title=None, ip=""):
        self.e2 = None
        self.ip = ip
        self.name = ""
        Dialog.__init__(self, parent, title)

    def body(self, master):

        tk.Label(master, text="A user at address " + self.ip + " is trying to contact you.").grid(row=0)

        tk.Label(master, text="Enter a Contact Name: ").grid(row=1)

        self.e2 = tk.Entry(master)
        self.e2.grid(row=1, column=1)

    def apply(self):
        self.name = self.e2.get()

        return self.name


class Login(Dialog):

    def __init__(self, parent, title=None):
        self.e1 = None
        self.e2 = None
        self.ip = None
        self.name = ""
        Dialog.__init__(self, parent, title)

    def body(self, master):

        # tk.Label(master, text="IP Address: ").grid(row=0)
        #
        # self.e1 = tk.Entry(master)
        # self.e1.grid(row=0, column=1)

        tk.Label(master, text="Username: ").grid(row=1)

        self.e2 = tk.Entry(master)
        self.e2.grid(row=1, column=1)

    def apply(self):
        # self.ip = self.e1.get()
        self.name = self.e2.get()

        return self.ip
