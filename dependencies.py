import customtkinter as ctk
import subprocess
import threading
import pkg_resources

class DependencyManager(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#ffffff")

        # === Judul ===
        title = ctk.CTkLabel(
            self,
            text="📦 Dependencies Manager",
            font=("Roboto", 24, "bold"),
            text_color="#1976D2"
        )
        title.pack(pady=15)

        # === Input library ===
        self.entry = ctk.CTkEntry(self, placeholder_text="Masukkan nama library (misal: requests)", width=400)
        self.entry.pack(pady=10)

        # === Tombol aksi ===
        btn_frame = ctk.CTkFrame(self, fg_color="#f9f9f9")
        btn_frame.pack(pady=10)

        self.btn_check = ctk.CTkButton(btn_frame, text="Cek Library", fg_color="#2196F3", command=self.check_dependency)
        self.btn_install = ctk.CTkButton(btn_frame, text="Install Library", fg_color="#4CAF50", command=self.install_dependency)
        self.btn_clear = ctk.CTkButton(btn_frame, text="Clear Output", fg_color="#E53935", command=self.clear_output)

        self.btn_check.pack(side="left", padx=10, pady=10)
        self.btn_install.pack(side="left", padx=10, pady=10)
        self.btn_clear.pack(side="left", padx=10, pady=10)

        # === Output area ===
        self.output = ctk.CTkTextbox(self, width=900, height=400, font=("Consolas", 11),
                                     fg_color="#ffffff", border_width=1, border_color="#e0e0e0", text_color="#000")
        self.output.pack(pady=10, padx=20, fill="both", expand=True)

    # === CEK DEPENDENSI ===
    def check_dependency(self):
        lib = self.entry.get().strip()
        if not lib:
            self._write("⚠️ Masukkan nama library terlebih dahulu.\n")
            return

        try:
            pkg_resources.get_distribution(lib)
            self._write(f"✅ Library '{lib}' sudah terinstal.\n")
        except pkg_resources.DistributionNotFound:
            self._write(f"❌ Library '{lib}' belum terinstal.\n")

    # === INSTALL DEPENDENSI ===
    def install_dependency(self):
        lib = self.entry.get().strip()
        if not lib:
            self._write("⚠️ Masukkan nama library sebelum install.\n")
            return

        self._write(f"⬇️ Menginstal '{lib}'...\n")
        threading.Thread(target=self._run_pip, args=(lib,), daemon=True).start()

    def _run_pip(self, lib):
        process = subprocess.Popen(
            ["python", "-m", "pip", "install", lib],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in process.stdout:
            self._write(line)
        self._write(f"✅ Instalasi '{lib}' selesai.\n\n")

    # === BERSIHKAN OUTPUT ===
    def clear_output(self):
        self.output.delete("1.0", "end")

    # === TULIS KE OUTPUT ===
    def _write(self, text):
        self.output.insert("end", text)
        self.output.see("end")
