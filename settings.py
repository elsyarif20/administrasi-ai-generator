import customtkinter as ctk

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#ffffff")

        # === Judul ===
        title = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=("Roboto", 24, "bold"),
            text_color="#1976D2"
        )
        title.pack(pady=15)

        # === Tema ===
        theme_label = ctk.CTkLabel(self, text="Tema Tampilan:", font=("Roboto", 14))
        theme_label.pack(pady=(20, 5))

        self.theme_menu = ctk.CTkOptionMenu(
            self,
            values=["Light", "Dark"],
            fg_color="#2196F3",
            command=self.change_theme
        )
        self.theme_menu.pack(pady=5)

        # === Ukuran Font ===
        font_label = ctk.CTkLabel(self, text="Ukuran Font Editor:", font=("Roboto", 14))
        font_label.pack(pady=(20, 5))

        self.font_menu = ctk.CTkOptionMenu(
            self,
            values=["10", "11", "12", "13", "14", "16"],
            fg_color="#2196F3",
            command=self.change_font_size
        )
        self.font_menu.pack(pady=5)

        # === Info ===
        self.info_label = ctk.CTkLabel(
            self,
            text="\nPerubahan tema langsung diterapkan.\nUkuran font akan aktif di editor baru.",
            font=("Roboto", 11),
            text_color="#666"
        )
        self.info_label.pack(pady=20)

    # === FUNGSI ===
    def change_theme(self, choice):
        if choice.lower() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def change_font_size(self, choice):
        # Simpan font size untuk modul lain jika ingin diterapkan global
        with open("font_size.txt", "w") as f:
            f.write(choice)
