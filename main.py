import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import time
import random
import json
import os
import sys
from datetime import datetime

# --- KONFIGURASI ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# File Data
USERS_FILE = 'users.json'        
DATA_FILE = 'typing_texts.json'  
HISTORY_FILE = 'history.json'    
STORY_FILE = 'story_mode.json'   

# Daftar Barang di Toko
SHOP_ITEMS = [
    {"icon": "🚗", "price": 0, "name": "Sedan (Default)"},
    {"icon": "🚕", "price": 150, "name": "Taksi"},
    {"icon": "🚙", "price": 300, "name": "SUV Biru"},
    {"icon": "🚌", "price": 450, "name": "Bus Kota"},
    {"icon": "🚑", "price": 600, "name": "Ambulans"},
    {"icon": "🚓", "price": 800, "name": "Polisi"},
    {"icon": "🏎️", "price": 1200, "name": "Formula 1"},
    {"icon": "🏍️", "price": 1500, "name": "Motor Sport"},
    {"icon": "🛸", "price": 3000, "name": "UFO Alien"},
    {"icon": "🚀", "price": 5000, "name": "Roket SpaceX"},
    {"icon": "🐉", "price": 9999, "name": "Naga Indosiar"}
]

class ModernTypingGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Python TypeRacer - Multi User Edition")
        self.state("zoomed")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.confirm_exit_options())

        # --- VARIABEL SYSTEM ---
        self.current_username = None
        self.user_data = {} 
        self.all_users_data = self.load_all_users()

        # Load Konten Game
        self.typing_texts = self.load_text_data()
        self.story_data = self.load_story_data()
        
        # Mapping Story
        self.story_map = {} 
        if "stories" in self.story_data:
            for key, val in self.story_data["stories"].items():
                self.story_map[val["title"]] = key 
        self.story_titles = list(self.story_map.keys())
        self.arcade_levels = list(self.typing_texts.keys())

        # Bot Profiles
        self.bot_profiles = self.get_bot_list()

        # Frame Containers
        self.login_container = None
        self.game_container = None

        # --- LOGIC ALUR MASUK ---
        self.check_auto_login()

    # =========================================
    # BAGIAN 1: SISTEM USER & LOGIN
    # =========================================

    def load_all_users(self):
        default_structure = {"last_login": "", "remember_me": False, "accounts": {}}
        if os.path.exists(USERS_FILE):
            try:
                with open(USERS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return default_structure
        return default_structure

    def save_all_users(self):
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump(self.all_users_data, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan data: {e}")

    def get_default_user_profile(self):
        achievements_template = {}
        if self.story_data and "stories" in self.story_data:
            for key, val in self.story_data["stories"].items():
                achievements_template[key] = {
                    "title": val["title"], "completed": False, "claimed": False, "reward": 500
                }

        return {
            "coins": 0,
            "owned_icons": ["🚗"],
            "current_icon": "🚗",
            "defeated_bots": [],
            "achievements": achievements_template
        }

    def check_auto_login(self):
        last_user = self.all_users_data.get("last_login")
        remember = self.all_users_data.get("remember_me", False)

        if remember and last_user and last_user in self.all_users_data.get("accounts", {}):
            self.perform_login(last_user)
        else:
            self.show_login_screen()

    def show_login_screen(self):
        if self.game_container:
            self.game_container.destroy()
            self.game_container = None
        
        self.login_container = ctk.CTkFrame(self, fg_color="transparent")
        self.login_container.pack(fill="both", expand=True)

        center_frame = ctk.CTkFrame(self.login_container, width=500, height=600, corner_radius=20)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center_frame, text="TYPE RACER LOGIN", font=("Roboto", 30, "bold")).pack(pady=30)

        # Tab View
        self.tab_login = ctk.CTkTabview(center_frame, width=400, height=300)
        self.tab_login.pack(pady=10)
        self.tab_login.add("Masuk")
        self.tab_login.add("Buat Akun")

        # --- TAB MASUK ---
        existing_users = list(self.all_users_data.get("accounts", {}).keys())
        
        ctk.CTkLabel(self.tab_login.tab("Masuk"), text="Pilih Akun:", font=("Roboto", 14)).pack(pady=(20, 5))
        self.user_select_menu = ctk.CTkOptionMenu(self.tab_login.tab("Masuk"), values=existing_users if existing_users else ["Belum ada akun"])
        self.user_select_menu.pack(pady=10)
        
        self.remember_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.tab_login.tab("Masuk"), text="Ingat Saya (Auto Login)", variable=self.remember_var).pack(pady=10)

        ctk.CTkButton(self.tab_login.tab("Masuk"), text="MASUK", width=200, height=40, font=("Roboto", 14, "bold"), 
                      command=self.handle_login_btn).pack(pady=20)

        # --- TAB BUAT AKUN ---
        ctk.CTkLabel(self.tab_login.tab("Buat Akun"), text="Nama Pengguna Baru:", font=("Roboto", 14)).pack(pady=(20, 5))
        self.new_user_entry = ctk.CTkEntry(self.tab_login.tab("Buat Akun"), placeholder_text="Contoh: Gamer123")
        self.new_user_entry.pack(pady=10)

        ctk.CTkButton(self.tab_login.tab("Buat Akun"), text="BUAT & MASUK", width=200, height=40, fg_color="#27AE60", 
                      font=("Roboto", 14, "bold"), command=self.handle_register_btn).pack(pady=20)

        # Tombol Keluar Apk
        ctk.CTkButton(center_frame, text="Keluar Aplikasi", fg_color="#C0392B", command=self.destroy).pack(pady=20)

    def handle_login_btn(self):
        selected = self.user_select_menu.get()
        if not selected or selected == "Belum ada akun":
            messagebox.showerror("Error", "Silakan pilih akun atau buat baru.")
            return
        
        self.all_users_data["last_login"] = selected
        self.all_users_data["remember_me"] = self.remember_var.get()
        self.save_all_users()
        self.perform_login(selected)

    def handle_register_btn(self):
        username = self.new_user_entry.get().strip()
        if not username:
            messagebox.showwarning("Warning", "Nama tidak boleh kosong.")
            return
        if username in self.all_users_data["accounts"]:
            messagebox.showerror("Error", "Nama pengguna sudah ada!")
            return
        
        self.all_users_data["accounts"][username] = self.get_default_user_profile()
        self.all_users_data["last_login"] = username
        self.all_users_data["remember_me"] = False 
        self.save_all_users()

        messagebox.showinfo("Sukses", f"Akun '{username}' berhasil dibuat!")
        self.perform_login(username)

    def perform_login(self, username):
        self.current_username = username
        self.user_data = self.all_users_data["accounts"][username]
        
        if self.login_container:
            self.login_container.destroy()
            self.login_container = None
        
        self.init_game_variables()
        self.create_game_ui()
        self.start_test()

    def confirm_exit_options(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Konfirmasi")
        dialog.geometry("400x250")
        dialog.attributes("-topmost", True)
        
        x = (self.winfo_screenwidth() // 2) - 200
        y = (self.winfo_screenheight() // 2) - 125
        dialog.geometry(f"400x250+{x}+{y}")

        ctk.CTkLabel(dialog, text="Apa yang ingin Anda lakukan?", font=("Roboto", 18, "bold")).pack(pady=20)

        def do_logout():
            dialog.destroy()
            self.handle_logout()

        def do_exit():
            dialog.destroy()
            self.destroy()

        ctk.CTkButton(dialog, text="🔄 Ganti Akun (Logout)", fg_color="#E67E22", command=do_logout).pack(pady=10, fill="x", padx=50)
        ctk.CTkButton(dialog, text="❌ Keluar Aplikasi", fg_color="#C0392B", command=do_exit).pack(pady=10, fill="x", padx=50)
        ctk.CTkButton(dialog, text="Batal", fg_color="gray", command=dialog.destroy).pack(pady=10)

    def handle_logout(self):
        self.all_users_data["remember_me"] = False
        self.save_all_users()
        self.current_username = None
        self.user_data = {}
        
        if self.game_container:
            self.game_container.destroy()
            self.game_container = None
        self.show_login_screen()

    # =========================================
    # BAGIAN 2: LOGIC GAME
    # =========================================

    def init_game_variables(self):
        self.current_level_var = ctk.StringVar(value=self.arcade_levels[0] if self.arcade_levels else "No Data")
        self.text_to_type = ""
        self.start_time = 0
        self.typing_started = False
        self.test_completed = False
        self.active_bot = None
        self.bot_animation_id = None
        
        self.is_story_mode = False 
        self.current_story_pack = [] 
        self.current_chapter_index = 0
        self.current_story_title = ""
        self.current_story_key = ""

    def save_current_user_data(self):
        if self.current_username:
            self.all_users_data["accounts"][self.current_username] = self.user_data
            self.save_all_users()

    def create_game_ui(self):
        self.game_container = ctk.CTkFrame(self, fg_color="transparent")
        self.game_container.pack(fill="both", expand=True)

        # 1. HEADER
        self.header_frame = ctk.CTkFrame(self.game_container, fg_color="transparent")
        self.header_frame.pack(pady=15, padx=30, fill='x')

        self.title_lbl = ctk.CTkLabel(self.header_frame, text=f"TYPE RACER | {self.current_username}", font=("Roboto", 28, "bold"))
        self.title_lbl.pack(side="left")

        self.progress_lbl = ctk.CTkLabel(self.header_frame, text="", font=("Roboto", 20, "bold"), text_color="#E67E22")
        self.progress_lbl.pack(side="left", padx=20)

        self.coin_lbl = ctk.CTkLabel(
            self.header_frame, 
            text=f"💰 {self.user_data['coins']}", 
            font=("Roboto", 24, "bold"), 
            text_color="#F1C40F"
        )
        self.coin_lbl.pack(side="right", padx=20)

        # 2. MENU BAR
        self.menu_frame = ctk.CTkFrame(self.game_container, fg_color="transparent")
        self.menu_frame.pack(pady=5, padx=30, fill='x')

        self.lvl_label = ctk.CTkLabel(self.menu_frame, text="Level:")
        self.lvl_label.pack(side="left", padx=(0,5))
        
        self.level_menu = ctk.CTkOptionMenu(
            self.menu_frame, variable=self.current_level_var, values=self.arcade_levels, 
            command=self.handle_level_change, width=220
        )
        self.level_menu.pack(side="left")

        btn_config = {"width": 100, "font": ("Roboto", 12, "bold")}
        
        self.btn_mode = ctk.CTkButton(self.menu_frame, text="📖 Mode Story", fg_color="#D35400", command=self.toggle_game_mode, width=120, font=("Roboto", 12, "bold"))
        self.btn_mode.pack(side="left", padx=10)

        # TOMBOL MENU KANAN
        self.btn_exit = ctk.CTkButton(self.menu_frame, text="🚪 Keluar", fg_color="#7B241C", command=self.confirm_exit_options, **btn_config)
        self.btn_exit.pack(side="right", padx=5)

        self.btn_reset = ctk.CTkButton(self.menu_frame, text="🔄 Reset", fg_color="#C0392B", command=self.start_test, **btn_config)
        self.btn_reset.pack(side="right", padx=5)

        self.btn_shop = ctk.CTkButton(self.menu_frame, text="🛒 Shop", fg_color="#2980B9", command=self.open_shop_window, **btn_config)
        self.btn_shop.pack(side="right", padx=5)
        
        self.btn_achieve = ctk.CTkButton(self.menu_frame, text="🏆 Pencapaian", fg_color="#F39C12", command=self.open_achievement_window, **btn_config)
        self.btn_achieve.pack(side="right", padx=5)

        # TOMBOL PERINGKAT (BARU)
        self.btn_rank = ctk.CTkButton(self.menu_frame, text="🥇 Peringkat", fg_color="#D4AC0D", command=self.open_leaderboard_window, **btn_config)
        self.btn_rank.pack(side="right", padx=5)

        self.btn_target = ctk.CTkButton(self.menu_frame, text="🎯 Target", fg_color="#8E44AD", command=self.open_target_window, **btn_config)
        self.btn_target.pack(side="right", padx=5)
        
        self.btn_history = ctk.CTkButton(self.menu_frame, text="📜 Riwayat", fg_color="#27AE60", command=self.open_history_window, **btn_config)
        self.btn_history.pack(side="right", padx=5)

        # 3. GAME AREA
        self.track_container = ctk.CTkFrame(self.game_container, fg_color="#2B2B2B", corner_radius=15)
        self.track_container.pack(pady=15, padx=30, fill='x')
        
        self.race_track = VisualRaceTrack(self.track_container, width=1000, height=150, bg="#2B2B2B", highlightthickness=0)
        self.race_track.pack(pady=10, padx=10, fill='both', expand=True)

        # 4. STATS
        self.stats_frame = ctk.CTkFrame(self.game_container, fg_color="transparent")
        self.stats_frame.pack(pady=5, padx=30, fill='x')
        self.stats_frame.columnconfigure((0,1,2), weight=1)

        self.card_bot = self.create_stat_card(self.stats_frame, 0, "Lawan", "...", "#E67E22")
        self.card_wpm = self.create_stat_card(self.stats_frame, 1, "WPM Saya", "0", "#3B8ED0")
        self.card_acc = self.create_stat_card(self.stats_frame, 2, "Akurasi", "100%", "#2CC985")

        # 5. INPUT & TEXT
        self.text_display = ctk.CTkTextbox(
            self.game_container, height=120, font=("Consolas", 20), text_color="#BDC3C7", 
            fg_color="#181818", wrap="word", corner_radius=10, border_width=2
        )
        self.text_display.pack(pady=15, padx=30, fill='x')
        self.text_display.tag_config("correct", foreground="#2CC985") 
        self.text_display.tag_config("wrong", foreground="#E74C3C", background="#582828")
        self.text_display.configure(state="disabled")

        self.input_entry = ctk.CTkEntry(
            self.game_container, height=50, font=("Consolas", 24), 
            placeholder_text="Ketik di sini...", border_color="#5F6A6A"
        )
        self.input_entry.pack(pady=(0, 20), padx=30, fill='x')
        self.input_entry.bind("<KeyRelease>", self.check_input)
        self.input_entry.bind("<Return>", lambda e: self.start_test())

        self.hint_lbl = ctk.CTkLabel(self.game_container, text="Tekan ENTER untuk Reset Cepat | ESC untuk Menu Keluar", text_color="gray")
        self.hint_lbl.pack(side="bottom", pady=10)

    # --- HELPER FUNCTIONS ---
    def get_bot_list(self):
        return [
            {"name": "Siput", "wpm": 10, "emoji": "🐌", "min_lvl": 0},
            {"name": "Kura-kura", "wpm": 20, "emoji": "🐢", "min_lvl": 0},
            {"name": "Koala", "wpm": 30, "emoji": "🐨", "min_lvl": 0},
            {"name": "Ayam", "wpm": 40, "emoji": "🐔", "min_lvl": 0},
            {"name": "Kucing", "wpm": 50, "emoji": "🐱", "min_lvl": 0},
            {"name": "Anjing", "wpm": 60, "emoji": "🐕", "min_lvl": 1},
            {"name": "Kuda", "wpm": 70, "emoji": "🐎", "min_lvl": 1},
            {"name": "Serigala", "wpm": 80, "emoji": "🐺", "min_lvl": 1},
            {"name": "Elang", "wpm": 90, "emoji": "🦅", "min_lvl": 1},
            {"name": "Cheetah", "wpm": 100, "emoji": "🐆", "min_lvl": 2},
            {"name": "Mobil F1", "wpm": 120, "emoji": "🏎️", "min_lvl": 2},
            {"name": "Pesawat", "wpm": 140, "emoji": "✈️", "min_lvl": 2},
            {"name": "Flash", "wpm": 160, "emoji": "⚡", "min_lvl": 3},
            {"name": "Alien", "wpm": 180, "emoji": "👽", "min_lvl": 3},
            {"name": "AI God", "wpm": 200, "emoji": "🤖", "min_lvl": 3}
        ]

    def create_stat_card(self, parent, col, title, value, color):
        frame = ctk.CTkFrame(parent, fg_color="#242424", corner_radius=10)
        frame.grid(row=0, column=col, padx=5, sticky="ew")
        ctk.CTkLabel(frame, text=title, font=("Roboto", 12), text_color="gray").pack(pady=(10,0))
        lbl = ctk.CTkLabel(frame, text=value, font=("Roboto", 24, "bold"), text_color=color)
        lbl.pack(pady=(0,10))
        return lbl

    def load_text_data(self):
        default = {"Level 1 (Mudah)": ["test"], "Level 2 (Sedang)": ["test"]}
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f: return json.load(f).get('level_data', default)
            except: pass
        return default

    def load_story_data(self):
        default_story = {
            "selected_story": "motivation_life",
            "stories": {
                "motivation_life": {
                    "title": "Motivasi Hidup",
                    "chapters": [
                        {"title": "Langkah Awal", "text": "Setiap perjalanan besar dimulai dengan satu langkah kecil."},
                        {"title": "Konsistensi", "text": "Konsistensi adalah kunci yang membedakan antara pemimpi dan pemenang."}
                    ]
                }
            }
        }
        if not os.path.exists(STORY_FILE):
            try:
                with open(STORY_FILE, 'w') as f: json.dump(default_story, f, indent=4)
            except: pass
            return default_story
        try:
            with open(STORY_FILE, 'r') as f: return json.load(f)
        except: return default_story

    # --- GAME MODE LOGIC ---
    def toggle_game_mode(self):
        self.is_story_mode = not self.is_story_mode
        
        if self.is_story_mode:
            if not self.story_titles:
                messagebox.showerror("Error", "Tidak ada cerita.")
                self.is_story_mode = False
                return

            self.title_lbl.configure(text=f"MODE CERITA | {self.current_username}", text_color="#F39C12")
            self.btn_mode.configure(text="🔙 Arcade Mode", fg_color="#7F8C8D")
            self.lvl_label.configure(text="Pilih Cerita:")
            self.level_menu.configure(values=self.story_titles)
            self.current_level_var.set(self.story_titles[0])
            self.load_story_pack_by_title(self.story_titles[0])
        else:
            self.title_lbl.configure(text=f"TYPE RACER | {self.current_username}", text_color="white")
            self.btn_mode.configure(text="📖 Mode Story", fg_color="#D35400")
            self.lvl_label.configure(text="Level:")
            self.progress_lbl.configure(text="") 
            self.level_menu.configure(values=self.arcade_levels)
            self.current_level_var.set(self.arcade_levels[0] if self.arcade_levels else "")
            
        self.start_test()

    def handle_level_change(self, choice):
        if self.is_story_mode:
            self.load_story_pack_by_title(choice)
        self.start_test()

    def load_story_pack_by_title(self, title):
        key = self.story_map.get(title)
        if not key: return

        pack = self.story_data["stories"].get(key)
        if pack:
            self.current_story_pack = pack["chapters"]
            self.current_story_title = pack["title"]
            self.current_story_key = key 
            self.current_chapter_index = 0
            self.update_story_progress_ui()

    def update_story_progress_ui(self):
        total = len(self.current_story_pack)
        current = self.current_chapter_index + 1
        self.progress_lbl.configure(text=f"Chapter {current} / {total}")

    # --- CORE GAMEPLAY ---
    def start_test(self):
        self.typing_started = False
        self.test_completed = False
        self.start_time = 0
        if self.bot_animation_id: self.after_cancel(self.bot_animation_id)

        if self.is_story_mode:
            if self.current_story_pack and self.current_chapter_index < len(self.current_story_pack):
                chapter_data = self.current_story_pack[self.current_chapter_index]
                self.text_to_type = chapter_data['text']
                chapter_title = chapter_data['title']
                self.card_bot.configure(text=f"📖 {chapter_title}")
                self.update_story_progress_ui()
            else:
                self.text_to_type = "Pilih cerita lain atau reset untuk mengulang."
                self.input_entry.configure(state="disabled")
                return
        else:
            selection = self.current_level_var.get()
            self.text_to_type = random.choice(self.typing_texts.get(selection, ["Error"]))
            
        self.total_chars = len(self.text_to_type)

        if self.is_story_mode:
             base_wpm = 30 + (self.current_chapter_index * 10) 
             self.active_bot = {"name": "Shadow", "wpm": base_wpm, "emoji": "👤", "min_lvl": 0}
             self.card_bot.configure(text=f"Ch.{self.current_chapter_index+1}: {self.current_story_pack[self.current_chapter_index]['title']}")
        else:
            idx_lvl = self.arcade_levels.index(self.current_level_var.get()) if self.current_level_var.get() in self.arcade_levels else 0
            candidates = [b for b in self.bot_profiles if b['min_lvl'] <= idx_lvl][-8:]
            self.active_bot = random.choice(candidates if candidates else self.bot_profiles)
            self.card_bot.configure(text=f"{self.active_bot['emoji']} {self.active_bot['name']} ({self.active_bot['wpm']})")

        self.bot_speed_per_sec = (self.active_bot['wpm'] / 60) * 5 / max(self.total_chars, 1)

        self.card_wpm.configure(text="0")
        self.card_acc.configure(text="100%")
        
        self.input_entry.configure(state="normal", border_color="#5F6A6A")
        self.input_entry.delete(0, "end")
        self.input_entry.focus()
        
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")
        self.text_display.insert("1.0", self.text_to_type)
        self.text_display.tag_remove("correct", "1.0", "end")
        self.text_display.tag_remove("wrong", "1.0", "end")
        self.text_display.configure(state="disabled")

        self.race_track.reset_track(self.active_bot, self.user_data['current_icon'])

    def check_input(self, event):
        if self.test_completed: return
        if event.keysym in ["Return", "Shift_L", "Shift_R", "Control_L"]: return

        current = self.input_entry.get()
        if not self.typing_started and len(current) > 0:
            self.typing_started = True
            self.start_time = time.time()
            self.animate_bot()

        self.text_display.configure(state="normal")
        self.text_display.tag_remove("correct", "1.0", "end")
        self.text_display.tag_remove("wrong", "1.0", "end")
        
        correct_count = 0
        for i, char in enumerate(current):
            if i >= len(self.text_to_type): break
            if char == self.text_to_type[i]:
                self.text_display.tag_add("correct", f"1.{i}", f"1.{i+1}")
                correct_count += 1
            else:
                self.text_display.tag_add("wrong", f"1.{i}", f"1.{i+1}")
        self.text_display.configure(state="disabled")

        self.race_track.update_user_pos(correct_count, self.total_chars)
        
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            wpm = round((len(current) / 5) / (elapsed / 60))
            self.card_wpm.configure(text=str(wpm))
            acc = round((correct_count / len(current)) * 100) if len(current) > 0 else 0
            self.card_acc.configure(text=f"{acc}%")

        if current == self.text_to_type:
            self.finish_game(won=True)

    def animate_bot(self):
        if self.test_completed: return
        elapsed = time.time() - self.start_time
        finished = self.race_track.update_bot_pos(elapsed, self.bot_speed_per_sec)
        if finished:
            self.finish_game(won=False)
        else:
            self.bot_animation_id = self.after(50, self.animate_bot)

    def finish_game(self, won):
        self.test_completed = True
        if self.bot_animation_id: self.after_cancel(self.bot_animation_id)
        self.input_entry.configure(state="disabled")
        
        final_wpm = int(self.card_wpm.cget("text"))
        reward = 0
        user_achievements = self.user_data.setdefault("achievements", {})

        if won:
            if self.is_story_mode:
                reward = 50 + (self.current_chapter_index * 10)
                self.input_entry.configure(border_color="#2CC985")
                
                if self.current_chapter_index + 1 >= len(self.current_story_pack):
                    key = self.current_story_key
                    if key in user_achievements:
                        if not user_achievements[key]["completed"]:
                            user_achievements[key]["completed"] = True
                            messagebox.showinfo("ACHIEVEMENT UNLOCKED!", f"Selamat! Anda menamatkan '{self.current_story_title}'.\nBuka menu Pencapaian untuk klaim hadiah.")

                    msg_title = "CERITA SELESAI! 🏆"
                    msg_body = f"Anda menamatkan: '{self.current_story_title}'.\n\nReward Akhir: +{reward} Koin"
                    self.current_chapter_index = 0
                else:
                    msg_title = "CHAPTER CLEAR"
                    msg_body = f"Lanjut ke chapter berikutnya...\nSpeed: {final_wpm} WPM\nReward: +{reward}"
                    self.current_chapter_index += 1 
            else:
                reward = 20 + final_wpm
                bot_name = self.active_bot['name']
                if bot_name not in self.user_data['defeated_bots']:
                    self.user_data['defeated_bots'].append(bot_name)
                msg_title = "MENANG! 🎉"
                msg_body = f"Hebat!\n\nKecepatan: {final_wpm} WPM\nHadiah: +{reward} Koin 💰"
        else:
            reward = 10
            self.input_entry.configure(border_color="#C0392B")
            msg_title = "KALAH"
            msg_body = f"Jangan menyerah!\nHadiah Hiburan: +{reward} Koin 💰"

        self.user_data['coins'] += reward
        self.save_current_user_data()
        self.coin_lbl.configure(text=f"💰 {self.user_data['coins']}")

        lvl_info = f"Story: {self.current_story_title} (Ch.{self.current_chapter_index})" if self.is_story_mode else self.current_level_var.get()
        self.save_history(final_wpm, self.card_acc.cget("text"), won, lvl_info)

        messagebox.showinfo(msg_title, msg_body)
        
        if self.is_story_mode and won:
            self.start_test()

    # --- POPUP WINDOWS ---

    def open_leaderboard_window(self):
        """Fitur Peringkat (Leaderboard) Baru"""
        win = ctk.CTkToplevel(self)
        win.title("Peringkat Global")
        win.geometry("500x600")
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="🥇 PERINGKAT PEMAIN", font=("Roboto", 24, "bold"), text_color="#F1C40F").pack(pady=10)
        ctk.CTkLabel(win, text="Diurutkan berdasarkan kekayaan koin", text_color="gray").pack(pady=(0, 10))

        # Header Table
        header_frame = ctk.CTkFrame(win, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        ctk.CTkLabel(header_frame, text="Rank", width=50, font=("Roboto", 12, "bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="User", width=150, anchor="w", font=("Roboto", 12, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Skin", width=50, font=("Roboto", 12, "bold")).pack(side="left")
        ctk.CTkLabel(header_frame, text="Koin", width=100, font=("Roboto", 12, "bold")).pack(side="left")

        scroll = ctk.CTkScrollableFrame(win)
        scroll.pack(pady=5, padx=10, fill="both", expand=True)

        # Ambil semua user dan urutkan
        accounts = self.all_users_data.get("accounts", {})
        leaderboard_data = []
        for name, data in accounts.items():
            leaderboard_data.append({
                "name": name,
                "coins": data.get("coins", 0),
                "icon": data.get("current_icon", "🚗")
            })
        
        # Sorting Descending by Coins
        leaderboard_data.sort(key=lambda x: x["coins"], reverse=True)

        for idx, user in enumerate(leaderboard_data):
            rank = idx + 1
            bg_color = "#34495E"
            
            # Warna Khusus Top 3
            if rank == 1: bg_color = "#D4AC0D" # Gold
            elif rank == 2: bg_color = "#7F8C8D" # Silver
            elif rank == 3: bg_color = "#A93226" # Bronze

            card = ctk.CTkFrame(scroll, fg_color=bg_color)
            card.pack(fill="x", pady=2)

            ctk.CTkLabel(card, text=f"#{rank}", width=50, font=("Roboto", 14, "bold")).pack(side="left")
            
            # Nama user (Bold jika itu user sendiri)
            name_font = ("Roboto", 14, "bold") if user['name'] == self.current_username else ("Roboto", 14)
            name_color = "#2ECC71" if user['name'] == self.current_username else "white"
            
            ctk.CTkLabel(card, text=user['name'], width=150, anchor="w", font=name_font, text_color=name_color).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=user['icon'], width=50, font=("Arial", 20)).pack(side="left")
            ctk.CTkLabel(card, text=f"💰 {user['coins']}", width=100, font=("Roboto", 14, "bold"), text_color="#F1C40F").pack(side="left")

    def open_achievement_window(self):
        win = ctk.CTkToplevel(self)
        win.title(f"Pencapaian - {self.current_username}")
        win.geometry("600x500")
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="🏆 PENCAPAIAN STORY", font=("Roboto", 24, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(win)
        scroll.pack(pady=10, padx=10, fill="both", expand=True)

        user_ach = self.user_data.get("achievements", {})

        for key, data in user_ach.items():
            card = ctk.CTkFrame(scroll, fg_color="#34495E")
            card.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(card, text=data['title'], font=("Roboto", 16, "bold")).pack(side="left", padx=15, pady=15)
            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(side="right", padx=10)

            if data['claimed']:
                ctk.CTkLabel(btn_frame, text="✅ SUDAH DIKLAIM", text_color="#2ECC71", font=("Roboto", 12, "bold")).pack()
            elif data['completed']:
                ctk.CTkButton(
                    btn_frame, 
                    text=f"KLAIM {data['reward']} 💰", 
                    fg_color="#F1C40F", 
                    text_color="black",
                    command=lambda k=key, w=win: self.claim_achievement(k, w)
                ).pack()
            else:
                ctk.CTkLabel(btn_frame, text="🔒 BELUM TAMAT", text_color="#E74C3C").pack()

    def claim_achievement(self, key, win_ref):
        user_ach = self.user_data.get("achievements", {})
        if key in user_ach:
            reward = user_ach[key]['reward']
            user_ach[key]['claimed'] = True
            
            self.user_data['coins'] += reward
            self.save_current_user_data()
            
            self.coin_lbl.configure(text=f"💰 {self.user_data['coins']}")
            # messagebox.showinfo("Sukses", f"Berhasil klaim {reward} Koin!")
            win_ref.destroy()
            self.open_achievement_window()

    def open_target_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Daftar Target")
        win.geometry("500x600")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="🎯 TARGET LIST", font=("Roboto", 24, "bold")).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(win, width=450, height=500)
        scroll.pack(pady=10, fill="both", expand=True)
        defeated = self.user_data['defeated_bots']
        for bot in self.bot_profiles:
            card = ctk.CTkFrame(scroll, fg_color="#242424")
            card.pack(fill="x", pady=5, padx=5)
            is_defeated = bot['name'] in defeated
            ctk.CTkLabel(card, text=bot['emoji'], font=("Arial", 30)).pack(side="left", padx=15, pady=10)
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="y")
            color = "#2CC985" if is_defeated else "white"
            status = "TERKALAHKAN ✅" if is_defeated else f"Speed: {bot['wpm']} WPM"
            ctk.CTkLabel(info, text=bot['name'], font=("Roboto", 16, "bold"), text_color=color, anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=status, font=("Roboto", 12), text_color="gray", anchor="w").pack(fill="x")

    def open_shop_window(self):
        win = ctk.CTkToplevel(self)
        win.title(f"Toko Kendaraan - {self.current_username}")
        win.geometry("600x500")
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text="🛒 SHOP", font=("Roboto", 24, "bold")).pack(pady=10)
        self.shop_coin_lbl = ctk.CTkLabel(win, text=f"Saldo Anda: 💰 {self.user_data['coins']}", font=("Roboto", 18), text_color="#F1C40F")
        self.shop_coin_lbl.pack(pady=5)
        scroll = ctk.CTkScrollableFrame(win)
        scroll.pack(pady=10, padx=10, fill="both", expand=True)
        
        for i, item in enumerate(SHOP_ITEMS):
            row = i // 2
            col = i % 2
            item_frame = ctk.CTkFrame(scroll, fg_color="#34495E")
            item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            ctk.CTkLabel(item_frame, text=item['icon'], font=("Arial", 40)).pack(pady=10)
            ctk.CTkLabel(item_frame, text=item['name'], font=("Roboto", 14, "bold")).pack()
            
            is_owned = item['icon'] in self.user_data['owned_icons']
            is_equipped = item['icon'] == self.user_data['current_icon']
            
            btn_text = "Beli"
            btn_color = "#2980B9"
            btn_state = "normal"
            cmd = lambda x=item: self.buy_item(x, win)
            
            if is_equipped:
                btn_text = "Dipakai"
                btn_color = "#27AE60"
                btn_state = "disabled"
            elif is_owned:
                btn_text = "Pakai"
                btn_color = "#E67E22"
                cmd = lambda x=item: self.equip_item(x, win)
            else:
                btn_text = f"💰 {item['price']}"
            
            ctk.CTkButton(item_frame, text=btn_text, fg_color=btn_color, state=btn_state, command=cmd).pack(pady=10, padx=20)
        
        scroll.columnconfigure(0, weight=1)
        scroll.columnconfigure(1, weight=1)

    def buy_item(self, item, win_ref):
        if self.user_data['coins'] >= item['price']:
            self.user_data['coins'] -= item['price']
            self.user_data['owned_icons'].append(item['icon'])
            self.save_current_user_data()
            self.coin_lbl.configure(text=f"💰 {self.user_data['coins']}")
            messagebox.showinfo("Sukses", f"Berhasil membeli {item['name']}!")
            win_ref.destroy()
            self.open_shop_window()
        else:
            messagebox.showerror("Gagal", "Uang tidak cukup!")

    def equip_item(self, item, win_ref):
        self.user_data['current_icon'] = item['icon']
        self.save_current_user_data()
        messagebox.showinfo("Sukses", f"Menggunakan {item['name']}.")
        win_ref.destroy()
        self.open_shop_window()
        if not self.typing_started:
            self.race_track.update_user_icon(item['icon'])

    def open_history_window(self):
        """Fitur Riwayat (Diperbarui dengan info Lawan)"""
        win = ctk.CTkToplevel(self)
        win.title(f"Riwayat - {self.current_username}")
        win.geometry("700x500") # Diperlebar sedikit
        win.attributes("-topmost", True)
        ctk.CTkLabel(win, text=f"📜 RIWAYAT: {self.current_username}", font=("Roboto", 24, "bold")).pack(pady=10)
        scroll_frame = ctk.CTkScrollableFrame(win, width=650, height=400)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        if not os.path.exists(HISTORY_FILE):
            ctk.CTkLabel(scroll_frame, text="Belum ada data pertandingan.", text_color="gray").pack(pady=20)
            return
        
        try:
            with open(HISTORY_FILE, 'r') as f: 
                raw_data = json.load(f)
                data = [d for d in raw_data if d.get('user') == self.current_username]
        except: return
        
        if not data:
            ctk.CTkLabel(scroll_frame, text="Belum ada riwayat untuk akun ini.", text_color="gray").pack(pady=20)
            return

        header_frame = ctk.CTkFrame(scroll_frame, fg_color="#34495E")
        header_frame.pack(fill="x", pady=5)
        
        # Kolom Header Baru
        headers = [("Tanggal", 90), ("Level", 120), ("VS Lawan", 120), ("WPM", 60), ("Hasil", 80)]
        for text, width in headers:
            ctk.CTkLabel(header_frame, text=text, font=("Roboto", 12, "bold"), width=width).pack(side="left", padx=5)
        
        for item in data:
            bg_color = "#1E8449" if item.get('result') == "WIN" else "#922B21"
            row = ctk.CTkFrame(scroll_frame, fg_color=bg_color)
            row.pack(fill="x", pady=2)
            
            # Format Data
            date_str = item.get('date', '-')[5:] # Ambil MM-DD HH:MM
            level_str = str(item.get('level', '?'))[:18]
            opponent_str = f"{item.get('opponent', 'Unknown')}"
            
            ctk.CTkLabel(row, text=date_str, width=90).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=level_str, width=120, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=opponent_str, width=120, anchor="w", font=("Roboto", 12, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(item.get('wpm', 0)), width=60).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=item.get('result', '-'), font=("Roboto", 12, "bold"), width=80).pack(side="left", padx=5)

    def save_history(self, wpm, acc, won, level_name):
        entry = {
            "user": self.current_username, 
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "level": level_name,
            "opponent": self.active_bot['name'] if not self.is_story_mode else "Story Bot",
            "wpm": wpm, "acc": acc, "result": "WIN" if won else "LOSE"
        }
        data = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f: data = json.load(f)
            except: pass
        data.insert(0, entry)
        try:
            with open(HISTORY_FILE, 'w') as f: json.dump(data, f, indent=4)
        except: pass

# --- VISUAL RACE TRACK ---
class VisualRaceTrack(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.width = kwargs.get('width', 1000)
        self.height = kwargs.get('height', 150)
        self.padding = 60
        self.lane_1 = 50; self.lane_2 = 100
        self.user_icon = "🚗"; self.bot_icon = "🐌"
        self.user_id = None; self.bot_id = None
        self.draw_track()

    def draw_track(self):
        self.create_rectangle(0, 0, self.width, self.height, fill="#2B2B2B", outline="")
        self.create_line(20, self.height/2, self.width-20, self.height/2, fill="#555555", dash=(15, 10), width=2)
        finish_x = self.width - self.padding
        self.create_line(finish_x, 10, finish_x, self.height-10, fill="#E74C3C", width=5)
        self.create_text(finish_x, 20, text="FINISH", fill="white", font=("Arial", 10, "bold"))
        self.create_text(10, self.lane_1, text="YOU", fill="#3B8ED0", anchor="w", font=("Arial", 12, "bold"))
        self.create_text(10, self.lane_2, text="BOT", fill="#E67E22", anchor="w", font=("Arial", 12, "bold"))
        self.user_id = self.create_text(self.padding, self.lane_1, text=self.user_icon, font=("Arial", 35))
        self.bot_id = self.create_text(self.padding, self.lane_2, text=self.bot_icon, font=("Arial", 35))

    def reset_track(self, bot_data, user_skin):
        self.user_icon = user_skin
        self.itemconfig(self.user_id, text=self.user_icon)
        self.itemconfig(self.bot_id, text=bot_data['emoji'])
        self.coords(self.user_id, self.padding, self.lane_1)
        self.coords(self.bot_id, self.padding, self.lane_2)

    def update_user_icon(self, icon):
        self.user_icon = icon
        self.itemconfig(self.user_id, text=icon)

    def update_user_pos(self, current, total):
        if total == 0: return
        track_len = self.width - (2 * self.padding)
        new_x = self.padding + ((current / total) * track_len)
        self.coords(self.user_id, new_x, self.lane_1)

    def update_bot_pos(self, elapsed, speed):
        track_len = self.width - (2 * self.padding)
        new_x = self.padding + ((elapsed * speed) * track_len)
        finish_x = self.width - self.padding
        final_x = min(new_x, finish_x)
        self.coords(self.bot_id, final_x, self.lane_2)
        return final_x >= finish_x

if __name__ == "__main__":
    app = ModernTypingGame()
    app.mainloop()