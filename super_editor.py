import sys
import os
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import webbrowser

# ==========================================================
# 🔧 FIX 1: Pastikan folder modules selalu bisa diimport
# ==========================================================
if getattr(sys, 'frozen', False):  # Saat dijalankan dari .exe
    BASE_PATH = sys._MEIPASS
else:  # Saat dijalankan dari Python langsung
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

MODULES_PATH = os.path.join(BASE_PATH, "modules")
if MODULES_PATH not in sys.path:
    sys.path.append(MODULES_PATH)

# ==========================================================
# 🔧 FIX 2: Fungsi resource_path untuk menemukan asset/icon
# ==========================================================
def resource_path(relative_path):
    """Dapatkan path absolut baik di dev mode atau dari bundle PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ==========================================================
# 🎨 SETUP MODE TAMPILAN
# ==========================================================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==========================================================
# 💻 KELAS UTAMA: Ahim Studio App
# ==========================================================
class AhimStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === JENDELA UTAMA ===
        self.title("Ahim Studio Code v7.2")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # === LOAD ICON SECARA AMAN ===
        icon_path = resource_path(os.path.join("assets", "icon.ico"))
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception as e:
                print(f"⚠️ Gagal memuat icon: {e}")
        else:
            print(f"❌ Icon tidak ditemukan di: {icon_path}")

        # === NAVBAR SAMPING ===
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#E3F2FD")
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="💎 Ahim Studio",
            font=("Roboto", 20, "bold"),
            text_color="#1976D2"
        )
        self.logo_label.pack(pady=(30, 20))

        # === MENU TOMBOL ===
        self.buttons = {
            "File Manager": lambda: self.load_module("modules.file_manager", "FileManagerFrame"),
            "Editor": lambda: self.load_module("modules.text_editor", "TextEditorFrame"),
            "Dependencies": lambda: self.load_module("modules.dependencies", "DependenciesFrame"),
            "MSI Builder": lambda: self.load_module("modules.builder", "BuilderFrame"),
            "Settings": lambda: self.load_module("modules.settings", "SettingsFrame"),
        }

        for name, cmd in self.buttons.items():
            btn = ctk.CTkButton(
                self.sidebar,
                text=name,
                corner_radius=6,
                fg_color="#2196F3",
                hover_color="#1976D2",
                command=cmd
            )
            btn.pack(pady=8, padx=10, fill="x")

        # === TOMBOL KELUAR ===
        ctk.CTkButton(
            self.sidebar,
            text="🚪 Keluar",
            fg_color="#E53935",
            hover_color="#B71C1C",
            command=self.quit
        ).pack(pady=(60, 10), padx=10, fill="x")

        # === AREA UTAMA (CONTENT) ===
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#FFFFFF")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="Selamat datang di Ahim Studio Code v7.2\n\nPilih menu di kiri untuk memulai.",
            font=("Roboto", 20, "bold"),
            text_color="#1976D2",
            justify="center"
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    # ======================================================
    # 🔁 FUNGSI UNTUK MEMUAT MODUL SECARA DINAMIS
    # ======================================================
    def load_module(self, module_name, class_name):
        try:
            # Bersihkan frame utama sebelum memuat modul baru
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Import dinamis
            module = __import__(module_name, fromlist=[class_name])
            frame_class = getattr(module, class_name)
            frame = frame_class(self.main_frame)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

        except ModuleNotFoundError:
            messagebox.showerror("Error", f"Modul '{module_name}' tidak ditemukan.\n\nPastikan folder 'modules/' sudah ikut ke bundle.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat modul:\n{e}")


# ==========================================================
# 🚀 JALANKAN APLIKASI
# ==========================================================
if __name__ == "__main__":
    app = AhimStudio()
    app.mainloop()
