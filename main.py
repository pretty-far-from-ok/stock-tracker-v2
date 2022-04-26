from app import Application
from tkinter import *


# driver
def main():
    root = Tk()
    root.title("Stock Tracker")
    root.geometry("630x575")  # width * height
    app = Application(root)
    root.mainloop()

main()

