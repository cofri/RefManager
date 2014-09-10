import Tkinter as tk
import time

class Example(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        tags = ['test 1','tag bla','coucou','trou noir']
        data = [[tag,False] for tag in tags]

        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="Tag", anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Label(self, text="Filter", anchor="w").grid(row=0, column=1, sticky="ew")


        row = 1
        for (tag, active) in data:
            nr_label = tk.Label(self, text=tag, anchor="w")
            active_cb = tk.Checkbutton(self, onvalue=True, offvalue=False)
            if active:
                active_cb.select()
            else:
                active_cb.deselect()

            nr_label.grid(row=row, column=0, sticky="ew")
            active_cb.grid(row=row, column=1, sticky="ew")


            row += 1

	tk.Button(self,text="Quit")


if __name__ == "__main__":
    root = tk.Tk()
    Example(root, text="Hello").pack(side="top", fill="both", expand=True, padx=10, pady=10)
    root.mainloop()

