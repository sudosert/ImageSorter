import ConstructForm

ConstructForm.construct_form()
#ConstructForm.root.after(1000, ConstructForm.update_output)
ConstructForm.root.protocol("WM_DELETE_WINDOW", ConstructForm.on_exit)
ConstructForm.root.mainloop()

