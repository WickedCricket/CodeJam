
# todo
# load hashes from hash file, for x in file get hash and  paste in text box in tkinter

from tkinter import *
root = Tk()
window_width = 1000
window_height = 500
window_x_pos = 2500
window_y_pos = 100

root.geometry(f'{window_width}x{window_height}+{window_x_pos}+{window_y_pos}')
Label(root, text="Hash Cracker", font=("Roboto", 30)).place(x= 100, y=0)
Label(root, text="test").place(x=50, y=40)
Label(root, text="test").place(x=75, y=80)

root.mainloop()