import customtkinter as ctk
from tkinter import filedialog, messagebox

class TextEditor(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#ffffff")

        # === Judul ===
        title = ctk.CTkLabel(
            self,
            text="✍️ Text Editor",
            font=("Roboto", 24, "bold"),
            text_color="#1976D2"
        )
        title.pack(pady=15)

        # === Toolbar Editor ===
        toolbar = ctk.CTkFrame(self, fg_color="#f9f9f9", height=50)
        toolbar.pack(padx=20, pady=10, fill="x")

        self.btn_open = ctk.CTkButton(toolbar, text="Buka File", width=100, fg_color="#2196F3", command=self.load_file)
        self.btn_save = ctk.CTkButton(toolbar, text="Simpan File", width=100, fg_color="#2196F3", command=self.save_file)
        self.btn_clear = ctk.CTkButton(toolbar, text="Bersihkan", width=100, fg_color="#E53935", command=self.clear_text)

        self.btn_open.pack(side="left", padx=10, pady=8)
        self.btn_save.pack(side="left", padx=10, pady=8)
        self.btn_clear.pack(side="left", padx=10, pady=8)

        # === Text Area ===
        self.textbox = ctk.CTkTextbox(self, width=950, height=500,
                                      font=("Roboto", 12),
                                      fg_color="#ffffff", border_width=1,
                                      border_color="#e0e0e0", text_color="#000")
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)

        # === Status ===
        self.file_path = None
        self.status_label = ctk.CTkLabel(self, text="Tidak ada file aktif",
                                         font=("Roboto", 11), text_color="#666")
        self.status_label.pack(pady=5)

    # === Fungsi File ===
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Buka File",
            filetypes=[("Semua File", "*.*"), ("File Teks", "*.txt"), ("Python Files", "*.py")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", data)
            self.file_path = file_path
            self.status_label.configure(text=f"File aktif: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka file:\n{e}")

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("File Teks", "*.txt"), ("Python Files", "*.py")]
            )
        if self.file_path:
            try:
                content = self.textbox.get("1.0", "end")
                with open(self.file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_label.configure(text=f"File disimpan: {self.file_path}")
                messagebox.showinfo("Berhasil", "File berhasil disimpan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file:\n{e}")

    def clear_text(self):
        confirm = messagebox.askyesno("Konfirmasi", "Hapus semua isi teks?")
        if confirm:
            self.textbox.delete("1.0", "end")
            self.status_label.configure(text="Editor kosong.")
