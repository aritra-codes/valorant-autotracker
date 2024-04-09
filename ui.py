import customtkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

root.mainloop()