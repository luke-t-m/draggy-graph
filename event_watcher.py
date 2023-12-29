import tkinter as tk

def test(event):
    print('Event:', event)

root = tk.Tk()

root.bind('<Key>', test)

root.bind('<Button>', test)

root.mainloop()