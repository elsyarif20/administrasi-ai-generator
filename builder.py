import customtkinter as ctk
import subprocess
import threading
import os
import webbrowser

class BuilderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#ffffff")

        # === Judul ===
        title = ctk.CTkLabel(
            self,
            text="🏗️ MSI Builder",
            font=("Roboto", 24, "bold"),
            text_color="#1976D2"
        )
        title.pack(pady=15)

        # === Input file utama ===
        self.py_entry = ctk.CTkEntry(self, placeholder_text="Masukkan nama file utama .py (misal: super_editor.py)", width=500)
        self.py_entry.pack(pady=10)

        # === Tombol Build ===
        self.build_btn = ctk.CTkButton(self, text="Build MSI", fg_color="#2196F3", command=self.start_build)
        self.build_btn.pack(pady=10)

        # === Output Log ===
        self.output = ctk.CTkTextbox(self, width=950, height=400, font=("Consolas", 11),
                                     fg_color="#ffffff", border_width=1, border_color="#e0e0e0", text_color="#000")
        self.output.pack(pady=15, padx=20, fill="both", expand=True)

        # === Status ===
        self.status_label = ctk.CTkLabel(self, text="Siap build MSI", font=("Roboto", 11), text_color="#666")
        self.status_label.pack(pady=(0, 10))

    # === MULAI PROSES BUILD ===
    def start_build(self):
        filename = self.py_entry.get().strip()
        if not filename:
            self._write("⚠️ Masukkan nama file .py dulu bro!\n")
            return

        if not os.path.exists(filename):
            self._write(f"❌ File '{filename}' tidak ditemukan di direktori ini.\n")
            return

        self.status_label.configure(text="Sedang build...")
        threading.Thread(target=self._build_process, args=(filename,), daemon=True).start()

    # === PROSES BUILD EXE + MSI ===
    def _build_process(self, filename):
        try:
            self._write(f"🚀 Memulai build MSI untuk {filename}...\n\n")

            # 1️⃣ Build EXE
            exe_cmd = f'pyinstaller --noconsole --onefile --icon=assets/icon.ico --name=AhimStudio {filename}'
            self._write(f"[RUN] {exe_cmd}\n\n")
            self._run_command(exe_cmd)

            # 2️⃣ Build MSI (gunakan path WiX kamu)
            wix_bin = r'"C:\Program Files (x86)\WiX Toolset v3.14\bin"'
            os.chdir("F:\\AhimStudio")  # ganti ke direktori project
            wix_cmd = (
                f'{wix_bin}\\candle.exe AhimStudio.wxs && '
                f'{wix_bin}\\light.exe AhimStudio.wixobj -ext WixUIExtension -o dist\\AhimStudio.msi'
            )
            self._write(f"\n[RUN] {wix_cmd}\n\n")
            self._run_command(wix_cmd)

            # 3️⃣ Selesai
            self._write("\n✅ Build MSI selesai! File tersimpan di folder /dist\n")
            self.status_label.configure(text="Build selesai ✅")

            # 4️⃣ Buka folder dist otomatis
            dist_path = os.path.abspath("dist")
            if os.path.exists(dist_path):
                webbrowser.open(dist_path)
                self._write(f"📂 Folder dibuka: {dist_path}\n")
            else:
                self._write("⚠️ Folder dist tidak ditemukan.\n")

        except Exception as e:
            self._write(f"❌ Error saat build: {e}\n")
            self.status_label.configure(text="Build gagal ❌")

    # === JALANKAN COMMAND TERMINAL DAN TAMPILKAN LOG ===
    def _run_command(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            self._write(line)
        process.wait()

    # === OUTPUT LOG ===
    def _write(self, text):
        self.output.insert("end", text)
        self.output.see("end")
