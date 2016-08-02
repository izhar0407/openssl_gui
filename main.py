#!/usr/bin/python

import sys
import Tkinter
import tkMessageBox
from openssl import crypto, compress_crypt


class openSSLApp(Tkinter.Tk):

  def __init__(self, parent):
    """create parent Tk window.
    """
    Tkinter.Tk.__init__(self, parent)
    self.parent = parent
    self.password = ''
    self.ciper = "aes-256-cbc"
    self.delete_fil = False
    self.initialize()

  def initialize(self):
    """initialize main tk window.
    """
    self.grid()

    button1 = Tkinter.Button(
        self, text=u"ENCRYPT", command=self.onEncClick)
    button1.grid(column=1, row=0, padx=10, pady=20)

    button2 = Tkinter.Button(
        self, text=u"DECRYPT", command=self.onDecClick)
    button2.grid(column=2, row=0, pady=20)

    button3 = Tkinter.Button(
        self, text=u"COMPRESS & ENCRYPT", command=self.onComClick)
    button3.grid(column=3, row=0, padx=10, pady=20)

    # set location of main window
    w = 370
    h = 100
    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()
    self.x = (ws/2) - (w/2)
    self.y = (hs/2) - (h/2)
    self.geometry('%dx%d+%d+%d' % (w, h, self.x, self.y-100))
    self.resizable(False, False)

  def onEncClick(self):
    """called when `encrypt` button is clicked
    """
    files = self.select_files()
    if files:
      self.pass_window()
      self.pass_level.wait_window()
      status = crypto(files, self.password, self.ciper, False, self.delete_fil)
      print status

  def onDecClick(self):
    """called when `decrypt` button is clicked
    """
    files = self.select_files()
    if files:
      self.pass_window()
      self.pass_level.wait_window()
      crypto(files, self.password, self.ciper, True, False)

  def onComClick(self):
    """called when `compress` button is clicked
    """
    dir_ = self.select_directory()
    if dir_ != "":
      self.pass_window()
      self.pass_level.wait_window()
      compress_crypt(dir_, self.password, self.ciper)

  def select_files(self):
    """function to open filedialogbox

    returns list of file selected
    if no file selected returns empty list
    """
    import tkFileDialog
    files = tkFileDialog.askopenfilenames(initialdir='~/Desktop')
    return list(files)

  def select_directory(self):
    """function to open filedialogbox

    returns list of file selected
    if no file selected returns empty list
    """
    import tkFileDialog
    dir_ = tkFileDialog.askdirectory()
    return dir_

  def pass_window(self):
    """create a password input window
    """
    self.pass_level = Tkinter.Toplevel()
    pwdbox = Tkinter.Entry(self.pass_level, show='*')
    self.pass_level.geometry('%dx%d+%d+%d' % (250, 180, self.x, self.y-100))

    def onpwdentry(evt):
      # Function to perform actions when <Return> key is pressed.
      if pwdbox.get() == verifybox.get():
        self.password = pwdbox.get()
        self.ciper = ciper_drop.get()
        if self.delete_var.get() == 1:
          self.delete_fil = True
        else:
          self.delete_fil = False
        self.pass_level.destroy()
      else:
        tkMessageBox.showerror("Error", "Password Dont Match")
        self.pass_level.wm_attributes("-topmost", 1)
        self.pass_level.focus_force()

    def onokclick():
      # Function to perform actions when OK button is clicked.
      if pwdbox.get() == verifybox.get():
        self.password = pwdbox.get()
        self.ciper = ciper_drop.get()
        if self.delete_var.get() == 1:
          self.delete_fil = True
        else:
          self.delete_fil = False
        self.pass_level.destroy()
      else:
        tkMessageBox.showerror("Error", "Passwords Dont Match")
        self.pass_level.wm_attributes("-topmost", 1)
        self.pass_level.focus_force()

    Tkinter.Label(self.pass_level, text='Enter Password').pack(side='top')
    pwdbox.pack(side='top')

    verifybox = Tkinter.Entry(self.pass_level, show='*')
    Tkinter.Label(self.pass_level, text='Verify Password').pack(side='top')

    verifybox.pack(side='top')
    verifybox.bind('<Return>', onpwdentry)
    self.delete_checkbox()
    lst1 = ['aes-256-cbc', 'aes-256-ebc', 'des-cbc']
    ciper_drop = Tkinter.StringVar(self.pass_level)
    ciper_drop.set("aes-256-cbc")
    drop = Tkinter.OptionMenu(self.pass_level, ciper_drop, *lst1)
    drop.pack(side='top')
    Tkinter.Button(
        self.pass_level, command=onokclick, text='OK').pack(side='top')

  def delete_checkbox(self):
    """add delete file checkbox to password window.
    """
    self.delete_var = Tkinter.BooleanVar()
    chkbttn = Tkinter.Checkbutton(
        self.pass_level, text="delete source files after operation? ",
        variable=self.delete_var, onvalue=True, offvalue=False)
    chkbttn.pack(side="bottom")


def check_compatibility():
  """checks compatibility

  Returns:
      bool: True if compatible else False.
  """
  compatible = True
  try:
    import tkFileDialog
  except:
    compatible = False
  if 'linux' not in sys.platform:
    compatible = False
  return compatible


if __name__ == "__main__":

  if not check_compatibility():
    print "Dependencies not met"
    exit(1)

  app = openSSLApp(None)
  app.title('OpenSSL GUI')
  app.mainloop()
