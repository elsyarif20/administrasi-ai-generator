import customtkinter as ctk
import os
import subprocess

class FileManagerFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#ffffff")

        title = ctk.CTkLabel(
            self, text="📂 File Manager",
            font=("Roboto", 24, "bold"),
            text_color="#1976D2"
        )
        title.pack(pady=15)

        # === Path input ===
        self.path_entry = ctk.CTkEntry(
            self,
            placeholder_text="Masukkan path folder (contoh: C:\\Users)",
            width=600
        )
        self.path_entry.pack(pady=10)

        self.open_btn = ctk.CTkButton(
            self,
            text="Buka Folder",
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.open_folder
        )
        self.open_btn.pack(pady=5)

        self.refresh_btn = ctk.CTkButton(
            self,
            text="Refresh",
            fg_color="#64B5F6",
            hover_color="#1976D2",
            command=self.refresh_list
        )
        self.refresh_btn.pack(pady=5)

        # === List file ===
        self.file_list = ctk.CTkTextbox(
            self,
            width=950,
            height=400,
            fg_color="#FAFAFA",
            text_color="#000",
            font=("Consolas", 11)
        )
        self.file_list.pack(pady=10, padx=10)

        self.status = ctk.CTkLabel(
            self,
            text="Siap eksplor folder.",
            font=("Roboto", 11),
            text_color="#777"
        )
        self.status.pack(pady=(0, 10))

    # === FUNGSI ===
    def open_folder(self):
        path = self.path_entry.get().strip()
        if not os.path.exists(path):
            self.status.configure(text=f"❌ Folder tidak ditemukan: {path}", text_color="#E53935")
            return
        subprocess.Popen(f'explorer "{path}"')
        self.status.configure(text=f"📂 Folder dibuka: {path}", text_color="#388E3C")

    def refresh_list(self):
        path = self.path_entry.get().strip()
        if not os.path.exists(path):
            self.file_list.delete("1.0", "end")
            self.file_list.insert("end", "❌ Path tidak valid.\n")
            return

        self.file_list.delete("1.0", "end")
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                self.file_list.insert("end", f"[DIR]  {item}\n")
            else:
                size = os.path.getsize(full_path)
                self.file_list.insert("end", f"{item}   ({size:,} bytes)\n")
        self.status.configure(text=f"✅ {len(os.listdir(path))} item ditemukan.")
