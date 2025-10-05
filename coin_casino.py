import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg=self['bg'], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self['bg'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.bind_mouse_wheel()

    def bind_mouse_wheel(self):
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

class CoinCasino:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Coin Casino")

        self.root.attributes('-fullscreen', True)

        self.root.configure(bg='#0d1b2a')

        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)

        self.balance = 100
        self.current_profile = None
        self.pending_animation = None
        self.fullscreen = True

        self.current_balance_label = None

        self.initialize_default_stats()
        self.initialize_default_achievements()
        self.initialize_default_shop()

        self.setup_directories()
        self.show_login_screen()

    def toggle_fullscreen(self, event=None):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        if not self.fullscreen:
            self.root.geometry("1200x800")

    def initialize_default_stats(self):
        """Initialize stats with all required keys"""
        self.stats = {
            "total_games": 0,
            "games_won": 0,
            "games_lost": 0,
            "total_winnings": 0,
            "total_losses": 0,
            "current_streak": 0,
            "longest_win_streak": 0,
            "longest_lose_streak": 0,
            "biggest_win": 0,
            "biggest_loss": 0
        }

    def initialize_default_achievements(self):
        """Initialize achievements with proper structure"""
        self.achievements = {
            "first_win": {"name": "First Blood", "description": "Win your first game", "unlocked": False},
            "high_roller": {"name": "High Roller", "description": "Bet 100 coins in one game", "unlocked": False},
            "rich": {"name": "Making It Rain", "description": "Reach 1000 coins", "unlocked": False},
            "gambler": {"name": "Addicted", "description": "Play 50 games", "unlocked": False},
            "lucky": {"name": "Lucky Streak", "description": "Win 5 games in a row", "unlocked": False}
        }

    def initialize_default_shop(self):
        """Initialize shop items with proper structure"""
        self.shop_items = {
            "lucky_charm": {"name": "Lucky Charm", "price": 50, "description": "Slightly increases win chances", "owned": False},
            "double_bet": {"name": "Double Bet", "price": 100, "description": "Unlocks 2x betting", "owned": False},
            "vip_pass": {"name": "VIP Pass", "price": 200, "description": "Daily bonus doubled", "owned": False}
        }

    def setup_directories(self):
        """Create necessary directories"""
        if not os.path.exists("profiles"):
            os.makedirs("profiles")

    def update_balance_display(self):
        """Update the current balance display"""
        if self.current_balance_label and isinstance(self.current_balance_label, tk.Label):
            try:
                self.current_balance_label.config(text=f"{self.balance}")
            except tk.TclError:
                pass

    def create_balance_display(self, parent):
        """Create a balance display and track it for updates"""
        balance_frame = tk.Frame(parent, bg='#1b263b', relief=tk.RAISED, bd=0)

        tk.Label(balance_frame, text="💰", font=("Arial", 14),
                bg='#1b263b', fg='#ffd166', padx=5, pady=8).pack(side=tk.LEFT)

        self.current_balance_label = tk.Label(balance_frame, text=f"{self.balance}", font=("Arial", 14, "bold"),
                                bg='#1b263b', fg='#ffd166', padx=5, pady=8)
        self.current_balance_label.pack(side=tk.LEFT)

        return balance_frame

    def show_login_screen(self):
        """Show login/registration screen"""
        self.clear_screen()
        self.current_balance_label = None

        main_container = tk.Frame(self.root, bg='#0d1b2a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        title_frame = tk.Frame(main_container, bg='#0d1b2a')
        title_frame.pack(pady=(0, 40))

        tk.Label(title_frame, text="🎰", font=("Arial", 60),
                bg='#0d1b2a', fg='#ffd166').pack()

        tk.Label(title_frame, text="COIN CASINO", font=("Arial", 36, "bold"),
                bg='#0d1b2a', fg='#e0e1dd').pack(pady=(10, 5))

        tk.Label(title_frame, text="Fortune Favors the Bold", font=("Arial", 14),
                bg='#0d1b2a', fg='#778da9').pack()

        login_box = tk.Frame(main_container, bg='#1b263b', relief=tk.RAISED, bd=0)
        login_box.pack(pady=20, padx=100, fill=tk.X)

        tk.Label(login_box, text="ENTER USERNAME", font=("Arial", 12, "bold"),
                bg='#1b263b', fg='#778da9').pack(pady=(20, 10))

        self.username_var = tk.StringVar()
        username_entry = tk.Entry(login_box, textvariable=self.username_var,
                                 font=("Arial", 14), bg='#415a77', fg='#e0e1dd',
                                 insertbackground='white', relief=tk.FLAT)
        username_entry.pack(pady=10, padx=40, fill=tk.X)
        username_entry.focus()

        button_frame = tk.Frame(login_box, bg='#1b263b')
        button_frame.pack(pady=20)

        self.create_modern_button(button_frame, "LOGIN", "#2a9d8f", self.login).grid(row=0, column=0, padx=10)
        self.create_modern_button(button_frame, "REGISTER", "#e76f51", self.register).grid(row=0, column=1, padx=10)

        username_entry.bind("<Return>", lambda e: self.login())

    def create_modern_button(self, parent, text, color, command):
        """Create a modern-looking button"""
        btn = tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                      command=command, bg=color, fg='white',
                      relief=tk.FLAT, bd=0, padx=30, pady=15,
                      cursor="hand2")
        def on_enter(e):
            btn['bg'] = self.lighten_color(color)
        def on_leave(e):
            btn['bg'] = color
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def lighten_color(self, color):
        """Lighten a hex color"""
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        lighter = tuple(min(255, c + 40) for c in rgb)
        return f'#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}'

    def login(self):
        """Login with existing profile"""
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return

        profile_path = f"profiles/{username}.json"
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r') as f:
                    data = json.load(f)

                self.current_profile = username
                self.balance = data.get("balance", 100)

                self.safe_load_stats(data.get("stats", {}))

                self.safe_load_achievements(data.get("achievements", {}))
                self.safe_load_shop(data.get("shop_items", {}))

                self.check_daily_bonus()
                self.show_main_menu()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load profile: {e}")
        else:
            messagebox.showerror("Error", "Profile not found. Please register first.")

    def safe_load_stats(self, loaded_stats):
        """Safely load stats with proper structure"""
        for key in self.stats:
            if key in loaded_stats:
                self.stats[key] = loaded_stats[key]
            else:
                self.stats[key] = 0

    def safe_load_achievements(self, loaded_achievements):
        """Safely load achievements with proper structure"""
        for key in self.achievements:
            if key in loaded_achievements:
                if isinstance(loaded_achievements[key], dict):
                    self.achievements[key]["unlocked"] = loaded_achievements[key].get("unlocked", False)
                else:
                    self.achievements[key]["unlocked"] = bool(loaded_achievements[key])
            else:
                self.achievements[key]["unlocked"] = False

    def safe_load_shop(self, loaded_shop):
        """Safely load shop items with proper structure"""
        for key in self.shop_items:
            if key in loaded_shop:
                if isinstance(loaded_shop[key], dict):
                    self.shop_items[key]["owned"] = loaded_shop[key].get("owned", False)
                else:
                    self.shop_items[key]["owned"] = bool(loaded_shop[key])
            else:
                self.shop_items[key]["owned"] = False

    def register(self):
        """Register new profile"""
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return

        profile_path = f"profiles/{username}.json"
        if not os.path.exists(profile_path):
            self.current_profile = username
            self.initialize_default_stats()
            self.initialize_default_achievements()
            self.initialize_default_shop()
            self.balance = 100
            self.save_profile()
            messagebox.showinfo("Success", f"Profile {username} created!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Username already exists!")

    def save_profile(self):
        """Save current profile data"""
        if not self.current_profile:
            return

        profile_path = f"profiles/{self.current_profile}.json"
        data = {
            "balance": self.balance,
            "stats": self.stats,
            "achievements": self.achievements,
            "shop_items": self.shop_items,
            "last_login": datetime.now().strftime("%Y-%m-%d")
        }

        try:
            with open(profile_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile: {e}")

    def check_daily_bonus(self):
        """Check and award daily login bonus"""
        profile_path = f"profiles/{self.current_profile}.json"
        today = datetime.now().strftime("%Y-%m-%d")

        try:
            with open(profile_path, 'r') as f:
                data = json.load(f)

            last_login = data.get("last_login", "")

            if last_login != today:
                bonus = 50 if self.shop_items["vip_pass"]["owned"] else 25
                self.balance += bonus
                self.update_balance_display()
                self.save_profile()
                messagebox.showinfo("Daily Bonus", f"Welcome back! You received {bonus} coins!")

        except:
            pass

    def show_main_menu(self):
        """Show main game menu"""
        self.clear_screen()
        self.current_balance_label = None

        main_container = tk.Frame(self.root, bg='#0d1b2a')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        header_frame = tk.Frame(main_container, bg='#0d1b2a')
        header_frame.pack(fill=tk.X, pady=(0, 30))

        user_frame = tk.Frame(header_frame, bg='#1b263b', relief=tk.RAISED, bd=0)
        user_frame.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(user_frame, text=f"👤 {self.current_profile}",
                font=("Arial", 12), bg='#1b263b', fg='#e0e1dd', padx=15, pady=8).pack(side=tk.LEFT)

        balance_frame = self.create_balance_display(header_frame)
        balance_frame.pack(side=tk.LEFT)

        title_frame = tk.Frame(main_container, bg='#0d1b2a')
        title_frame.pack(pady=(0, 40))

        tk.Label(title_frame, text="🎰", font=("Arial", 50),
                bg='#0d1b2a', fg='#ffd166').pack()
        tk.Label(title_frame, text="CHOOSE YOUR GAME", font=("Arial", 24, "bold"),
                bg='#0d1b2a', fg='#e0e1dd').pack(pady=(10, 5))

        games_frame = tk.Frame(main_container, bg='#0d1b2a')
        games_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        games = [
            ("🎲", "Coin Flip", "Heads or Tails?", self.show_coin_flip, "#2a9d8f"),
            ("🎰", "Slot Machine", "Spin to Win!", self.show_slot_machine, "#e76f51"),
            ("🎯", "Number Guess", "Guess 1-10", self.show_number_guess, "#e9c46a"),
            ("🃏", "Blackjack", "Coming Soon", self.show_blackjack, "#778da9")
        ]

        for i, (emoji, name, desc, command, color) in enumerate(games):
            row, col = i // 2, i % 2
            self.create_game_card(games_frame, emoji, name, desc, command, color).grid(
                row=row, column=col, padx=15, pady=15, sticky="nsew")

        games_frame.grid_rowconfigure(0, weight=1)
        games_frame.grid_rowconfigure(1, weight=1)
        games_frame.grid_columnconfigure(0, weight=1)
        games_frame.grid_columnconfigure(1, weight=1)

        bottom_frame = tk.Frame(main_container, bg='#0d1b2a')
        bottom_frame.pack(pady=30)

        menu_buttons = [
            ("📊", "STATS", self.show_statistics, "#9b59b6"),
            ("🏆", "ACHIEVEMENTS", self.show_achievements, "#e67e22"),
            ("🛍️", "SHOP", self.show_shop, "#27ae60"),
            ("🚪", "LOGOUT", self.show_login_screen, "#e74c3c")
        ]

        for i, (emoji, text, command, color) in enumerate(menu_buttons):
            btn = self.create_modern_button(bottom_frame, f"{emoji} {text}", color, command)
            btn.grid(row=0, column=i, padx=8)

    def create_game_card(self, parent, emoji, title, description, command, color):
        """Create a modern game card"""
        card = tk.Frame(parent, bg='#1b263b', relief=tk.RAISED, bd=0)

        tk.Label(card, text=emoji, font=("Arial", 40),
                bg='#1b263b', fg=color).pack(pady=(20, 10))

        tk.Label(card, text=title, font=("Arial", 16, "bold"),
                bg='#1b263b', fg='#e0e1dd').pack()

        tk.Label(card, text=description, font=("Arial", 10),
                bg='#1b263b', fg='#778da9').pack(pady=(5, 15))

        play_btn = tk.Button(card, text="PLAY →", font=("Arial", 12, "bold"),
                           command=command, bg=color, fg='white',
                           relief=tk.FLAT, bd=0, padx=20, pady=8,
                           cursor="hand2")
        play_btn.pack(pady=(0, 20))

        def on_enter(e):
            card.configure(bg='#23334d')
            play_btn['bg'] = self.lighten_color(color)
        def on_leave(e):
            card.configure(bg='#1b263b')
            play_btn['bg'] = color

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        play_btn.bind("<Enter>", on_enter)
        play_btn.bind("<Leave>", on_leave)

        return card

    def show_coin_flip(self):
        """Coin Flip Game"""
        self.clear_screen()
        if self.pending_animation:
            self.root.after_cancel(self.pending_animation)
            self.pending_animation = None

        main_frame = tk.Frame(self.root, bg='#0d1b2a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.create_game_header(main_frame, "🎲 Coin Flip", "Heads or Tails?")

        bet_frame = tk.Frame(main_frame, bg='#1b263b', relief=tk.RAISED, bd=0)
        bet_frame.pack(pady=30, padx=100, fill=tk.X)

        tk.Label(bet_frame, text="BET AMOUNT", font=("Arial", 12, "bold"),
                bg='#1b263b', fg='#778da9').pack(pady=(20, 10))

        self.bet_amount = tk.IntVar(value=10)

        bet_slider = tk.Scale(bet_frame, from_=1, to=min(500, self.balance),
                             orient=tk.HORIZONTAL, variable=self.bet_amount,
                             length=300, bg='#1b263b', fg='#e0e1dd',
                             highlightbackground='#1b263b', troughcolor='#415a77')
        bet_slider.pack(pady=10)

        quick_bet_frame = tk.Frame(bet_frame, bg='#1b263b')
        quick_bet_frame.pack(pady=15)

        for amount in [10, 25, 50, 100]:
            if amount <= self.balance:
                btn = tk.Button(quick_bet_frame, text=str(amount), font=("Arial", 10),
                              command=lambda a=amount: self.bet_amount.set(a),
                              bg='#415a77', fg='white', relief=tk.FLAT, width=4)
                btn.pack(side=tk.LEFT, padx=5)

        coin_frame = tk.Frame(main_frame, bg='#0d1b2a')
        coin_frame.pack(pady=30)

        self.coin_label = tk.Label(coin_frame, text="🎰", font=("Arial", 100),
                                  bg='#0d1b2a', fg='#ffd166')
        self.coin_label.pack()

        choice_frame = tk.Frame(main_frame, bg='#0d1b2a')
        choice_frame.pack(pady=20)

        self.heads_button = self.create_modern_button(choice_frame, "HEADS", "#e76f51",
                                                     lambda: self.flip_coin("heads"))
        self.heads_button.grid(row=0, column=0, padx=20)

        self.tails_button = self.create_modern_button(choice_frame, "TAILS", "#2a9d8f",
                                                     lambda: self.flip_coin("tails"))
        self.tails_button.grid(row=0, column=1, padx=20)

    def create_game_header(self, parent, title, subtitle):
        """Create consistent game header"""
        header_frame = tk.Frame(parent, bg='#0d1b2a')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        back_btn = tk.Button(header_frame, text="← MENU", font=("Arial", 10, "bold"),
                           command=self.show_main_menu, bg='#415a77', fg='white',
                           relief=tk.FLAT, padx=15, pady=5, cursor="hand2")
        back_btn.pack(side=tk.LEFT)

        title_frame = tk.Frame(header_frame, bg='#0d1b2a')
        title_frame.pack(side=tk.LEFT, expand=True)

        tk.Label(title_frame, text=title, font=("Arial", 24, "bold"),
                bg='#0d1b2a', fg='#e0e1dd').pack()
        tk.Label(title_frame, text=subtitle, font=("Arial", 12),
                bg='#0d1b2a', fg='#778da9').pack()

        balance_frame = self.create_balance_display(header_frame)
        balance_frame.pack(side=tk.RIGHT)

    def flip_coin(self, choice):
        """Execute coin flip game logic"""
        bet = self.bet_amount.get()

        if bet > self.balance:
            messagebox.showerror("Error", "Not enough coins!")
            return

        if bet <= 0:
            messagebox.showerror("Error", "Bet must be positive!")
            return

        self.heads_button.config(state=tk.DISABLED)
        self.tails_button.config(state=tk.DISABLED)

        self.animate_coin_flip(choice, bet)

    def animate_coin_flip(self, choice, bet, frame=0):
        """Animate coin flip with smooth transitions"""
        frames = ["⚪", "🟡", "⚪", "🟡", "⚪", "🟡", "⚪"]

        if frame < len(frames):
            self.coin_label.config(text=frames[frame])
            self.pending_animation = self.root.after(150, lambda: self.animate_coin_flip(choice, bet, frame + 1))
        else:
            result = random.choice(["heads", "tails"])
            win_multiplier = 1.95 if self.shop_items["lucky_charm"]["owned"] else 1.9

            if result == choice:
                win_amount = int(bet * win_multiplier)
                self.balance += win_amount
                self.coin_label.config(text="🪙" if result == "heads" else "💰")
                messagebox.showinfo("Winner!", f"You won {win_amount} coins!")

                self.update_stats(win=win_amount, bet=bet)
            else:
                self.balance -= bet
                self.coin_label.config(text="🪙" if result == "heads" else "💰")
                messagebox.showinfo("Lost", f"You lost {bet} coins!")

                self.update_stats(loss=bet)

            self.update_balance_display()
            self.check_achievements()
            self.save_profile()

            self.heads_button.config(state=tk.NORMAL)
            self.tails_button.config(state=tk.NORMAL)
            self.pending_animation = None

    def update_stats(self, win=0, loss=0, bet=0):
        """Update game statistics"""
        if win > 0:
            self.stats["games_won"] += 1
            self.stats["total_winnings"] += win
            self.stats["current_streak"] = max(0, self.stats["current_streak"]) + 1
            self.stats["longest_win_streak"] = max(self.stats["longest_win_streak"], self.stats["current_streak"])
            self.stats["biggest_win"] = max(self.stats["biggest_win"], win)
        else:
            self.stats["games_lost"] += 1
            self.stats["total_losses"] += loss
            self.stats["current_streak"] = min(0, self.stats["current_streak"]) - 1
            self.stats["longest_lose_streak"] = min(self.stats["longest_lose_streak"], self.stats["current_streak"])
            self.stats["biggest_loss"] = max(self.stats["biggest_loss"], loss)

        self.stats["total_games"] += 1

    def show_slot_machine(self):
        """Slot Machine Game"""
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#0d1b2a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.create_game_header(main_frame, "🎰 Slot Machine", "Spin to Win!")

        bet_frame = tk.Frame(main_frame, bg='#1b263b', relief=tk.RAISED, bd=0)
        bet_frame.pack(pady=30, padx=100, fill=tk.X)

        tk.Label(bet_frame, text="BET AMOUNT", font=("Arial", 12, "bold"),
                bg='#1b263b', fg='#778da9').pack(pady=(20, 10))

        self.slot_bet = tk.IntVar(value=10)
        bet_slider = tk.Scale(bet_frame, from_=1, to=min(500, self.balance),
                             orient=tk.HORIZONTAL, variable=self.slot_bet,
                             length=300, bg='#1b263b', fg='#e0e1dd',
                             highlightbackground='#1b263b', troughcolor='#415a77')
        bet_slider.pack(pady=10)

        reels_frame = tk.Frame(main_frame, bg='#0d1b2a')
        reels_frame.pack(pady=40)

        self.reel_labels = []
        reel_container = tk.Frame(reels_frame, bg='#1b263b', relief=tk.SUNKEN, bd=2)
        reel_container.pack(pady=20)

        for i in range(3):
            label = tk.Label(reel_container, text="🍒", font=("Arial", 50),
                           bg='#415a77', fg='white', width=4, height=2,
                           relief=tk.RAISED, bd=3)
            label.pack(side=tk.LEFT, padx=10, pady=20)
            self.reel_labels.append(label)

        self.spin_button = self.create_modern_button(main_frame, "🎰 SPIN 🎰", "#e76f51", self.spin_slots)
        self.spin_button.pack(pady=20)

    def spin_slots(self):
        """Spin the slot machine"""
        bet = self.slot_bet.get()

        if bet > self.balance:
            messagebox.showerror("Error", "Not enough coins!")
            return

        self.spin_button.config(state=tk.DISABLED)
        self.animate_slot_spin(bet)

    def animate_slot_spin(self, bet, spin_count=0):
        """Animate slot machine spin"""
        symbols = ["🍒", "🍋", "🔔", "⭐", "🍊", "💎"]

        if spin_count < 10:
            for label in self.reel_labels:
                label.config(text=random.choice(symbols))
            self.pending_animation = self.root.after(100, lambda: self.animate_slot_spin(bet, spin_count + 1))
        else:
            results = [random.choice(symbols) for _ in range(3)]
            for i, label in enumerate(self.reel_labels):
                label.config(text=results[i])

            if results[0] == results[1] == results[2]:
                win_amount = bet * 10
                self.balance += win_amount
                messagebox.showinfo("JACKPOT!", f"All {results[0]}! You won {win_amount} coins!")
                self.update_stats(win=win_amount)
            else:
                self.balance -= bet
                messagebox.showinfo("No Win", "Better luck next time!")
                self.update_stats(loss=bet)

            self.update_balance_display()
            self.check_achievements()
            self.save_profile()
            self.spin_button.config(state=tk.NORMAL)
            self.pending_animation = None

    def show_number_guess(self):
        """Number Guessing Game"""
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#0d1b2a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.create_game_header(main_frame, "🎯 Number Guess", "Pick 1-10, Win 5x!")

        info_frame = tk.Frame(main_frame, bg='#1b263b', relief=tk.RAISED, bd=0)
        info_frame.pack(pady=20, padx=100, fill=tk.X)

        tk.Label(info_frame, text="Guess a number between 1-10\nWin 5x your bet!",
                font=("Arial", 12), bg='#1b263b', fg='#e0e1dd',
                justify=tk.CENTER, pady=20).pack()

        bet_frame = tk.Frame(main_frame, bg='#0d1b2a')
        bet_frame.pack(pady=20)

        tk.Label(bet_frame, text="BET:", font=("Arial", 12),
                bg='#0d1b2a', fg='#e0e1dd').grid(row=0, column=0, padx=5)

        self.guess_bet = tk.IntVar(value=10)
        bet_entry = tk.Entry(bet_frame, textvariable=self.guess_bet,
                           font=("Arial", 12), bg='#415a77', fg='#e0e1dd',
                           relief=tk.FLAT, width=10)
        bet_entry.grid(row=0, column=1, padx=5)

        number_frame = tk.Frame(main_frame, bg='#0d1b2a')
        number_frame.pack(pady=30)

        self.number_var = tk.IntVar()
        for i in range(1, 11):
            rb = tk.Radiobutton(number_frame, text=str(i), variable=self.number_var,
                              value=i, font=("Arial", 14, "bold"),
                              bg='#0d1b2a', fg='#e0e1dd', selectcolor='#2a9d8f',
                              indicatoron=0, width=3, height=2,
                              relief=tk.RAISED)
            rb.grid(row=(i-1)//5, column=(i-1)%5, padx=5, pady=5)

        self.guess_button = self.create_modern_button(main_frame, "🎯 GUESS", "#e9c46a", self.make_guess)
        self.guess_button.pack(pady=20)

        self.guess_result = tk.Label(main_frame, text="", font=("Arial", 14, "bold"),
                                    bg='#0d1b2a', fg='#ffd166')
        self.guess_result.pack(pady=10)

    def make_guess(self):
        """Process number guess"""
        bet = self.guess_bet.get()
        guess = self.number_var.get()

        if not guess:
            messagebox.showerror("Error", "Please select a number!")
            return

        if bet > self.balance:
            messagebox.showerror("Error", "Not enough coins!")
            return

        target = random.randint(1, 10)

        if guess == target:
            win_amount = bet * 5
            self.balance += win_amount
            self.guess_result.config(text=f"🎉 Correct! You won {win_amount} coins!")
            self.update_stats(win=win_amount)
        else:
            self.balance -= bet
            self.guess_result.config(text=f"❌ Wrong! The number was {target}")
            self.update_stats(loss=bet)

        self.update_balance_display()
        self.check_achievements()
        self.save_profile()

    def show_blackjack(self):
        """Simple Blackjack Game"""
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg='#0d1b2a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.create_game_header(main_frame, "🃏 Blackjack", "Coming Soon!")

        coming_frame = tk.Frame(main_frame, bg='#1b263b', relief=tk.RAISED, bd=0)
        coming_frame.pack(expand=True, fill=tk.BOTH, padx=100, pady=100)

        tk.Label(coming_frame, text="🃏", font=("Arial", 60),
                bg='#1b263b', fg='#778da9').pack(pady=(50, 20))

        tk.Label(coming_frame, text="Blackjack Coming Soon!", font=("Arial", 20, "bold"),
                bg='#1b263b', fg='#e0e1dd').pack(pady=10)

        tk.Label(coming_frame, text="This exciting game will be available\nin the next update!",
                font=("Arial", 12), bg='#1b263b', fg='#778da9',
                justify=tk.CENTER).pack(pady=20)

    def show_statistics(self):
        """Show player statistics in a scrollable window"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Player Statistics")
        stats_window.geometry("800x700")
        stats_window.resizable(True, True)
        stats_window.configure(bg='#0d1b2a')

        header_frame = tk.Frame(stats_window, bg='#0d1b2a')
        header_frame.pack(fill=tk.X, padx=30, pady=20)

        tk.Label(header_frame, text="📊", font=("Arial", 30),
                bg='#0d1b2a', fg='#ffd166').pack()
        tk.Label(header_frame, text="PLAYER STATISTICS", font=("Arial", 20, "bold"),
                bg='#0d1b2a', fg='#e0e1dd').pack(pady=5)

        scrollable_stats = ScrollableFrame(stats_window, bg='#0d1b2a')
        scrollable_stats.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        win_rate = (self.stats["games_won"] / self.stats["total_games"] * 100) if self.stats["total_games"] > 0 else 0
        net_profit = self.stats["total_winnings"] - self.stats["total_losses"]

        stat_cards = [
            ("🎯", "Total Games", f"{self.stats['total_games']}", "#2a9d8f"),
            ("🏆", "Games Won", f"{self.stats['games_won']}", "#27ae60"),
            ("💔", "Games Lost", f"{self.stats['games_lost']}", "#e74c3c"),
            ("📈", "Win Rate", f"{win_rate:.1f}%", "#9b59b6"),
            ("💰", "Total Winnings", f"{self.stats['total_winnings']} coins", "#f1c40f"),
            ("💸", "Total Losses", f"{self.stats['total_losses']} coins", "#e67e22"),
            ("📊", "Net Profit", f"{net_profit} coins", "#3498db" if net_profit >= 0 else "#e74c3c"),
            ("🔥", "Current Streak", f"{self.stats['current_streak']}", "#e74c3c"),
            ("⭐", "Longest Win Streak", f"{self.stats['longest_win_streak']}", "#27ae60"),
            ("💀", "Longest Lose Streak", f"{abs(self.stats['longest_lose_streak'])}", "#e74c3c"),
            ("🎰", "Biggest Win", f"{self.stats['biggest_win']} coins", "#f1c40f"),
            ("📉", "Biggest Loss", f"{self.stats['biggest_loss']} coins", "#e67e22"),
            ("👤", "Player", f"{self.current_profile}", "#3498db"),
            ("💎", "Balance", f"{self.balance} coins", "#9b59b6")
        ]

        stats_container = scrollable_stats.scrollable_frame

        for i, (emoji, title, value, color) in enumerate(stat_cards):
            row, col = i // 2, i % 2
            card = tk.Frame(stats_container, bg='#1b263b', relief=tk.RAISED, bd=0)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            tk.Label(card, text=emoji, font=("Arial", 20),
                    bg='#1b263b', fg=color).pack(pady=(15, 5))
            tk.Label(card, text=title, font=("Arial", 10),
                    bg='#1b263b', fg='#778da9').pack()
            tk.Label(card, text=value, font=("Arial", 16, "bold"),
                    bg='#1b263b', fg='#e0e1dd').pack(pady=(5, 15))

        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)

        tk.Button(stats_window, text="CLOSE", font=("Arial", 12, "bold"),
                 command=stats_window.destroy, bg='#e74c3c', fg='white',
                 relief=tk.FLAT, padx=30, pady=10, cursor="hand2").pack(pady=20)

    def show_achievements(self):
        """Show achievements in a scrollable window"""
        achievements_window = tk.Toplevel(self.root)
        achievements_window.title("Achievements")
        achievements_window.geometry("700x700")
        achievements_window.resizable(True, True)
        achievements_window.configure(bg='#0d1b2a')

        header_frame = tk.Frame(achievements_window, bg='#0d1b2a')
        header_frame.pack(fill=tk.X, padx=30, pady=20)

        tk.Label(header_frame, text="🏆", font=("Arial", 30),
                bg='#0d1b2a', fg='#ffd166').pack()
        tk.Label(header_frame, text="ACHIEVEMENTS", font=("Arial", 20, "bold"),
                bg='#0d1b2a', fg='#e0e1dd').pack(pady=5)

        unlocked_count = sum(1 for a in self.achievements.values() if a["unlocked"])
        total_count = len(self.achievements)
        progress_frame = tk.Frame(header_frame, bg='#0d1b2a')
        progress_frame.pack(pady=10)

        tk.Label(progress_frame, text=f"Progress: {unlocked_count}/{total_count}",
                font=("Arial", 12, "bold"), bg='#0d1b2a', fg='#ffd166').pack()

        scrollable_achievements = ScrollableFrame(achievements_window, bg='#0d1b2a')
        scrollable_achievements.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        container = scrollable_achievements.scrollable_frame

        for key, achievement in self.achievements.items():
            status = "✅ UNLOCKED" if achievement["unlocked"] else "🔒 LOCKED"
            color = "#27ae60" if achievement["unlocked"] else "#7f8c8d"
            bg_color = "#1b263b" if achievement["unlocked"] else "#1b263b"

            card = tk.Frame(container, bg=bg_color, relief=tk.RAISED, bd=0)
            card.pack(fill=tk.X, padx=10, pady=8)

            status_frame = tk.Frame(card, bg=color, width=5)
            status_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

            content_frame = tk.Frame(card, bg=bg_color)
            content_frame.pack(fill=tk.X, padx=15, pady=15)

            tk.Label(content_frame, text=achievement["name"], font=("Arial", 14, "bold"),
                    bg=bg_color, fg=color).pack(anchor=tk.W)
            tk.Label(content_frame, text=achievement["description"], font=("Arial", 10),
                    bg=bg_color, fg='#e0e1dd').pack(anchor=tk.W)
            tk.Label(content_frame, text=status, font=("Arial", 10, "bold"),
                    bg=bg_color, fg=color).pack(anchor=tk.W, pady=(5, 0))

        tk.Button(achievements_window, text="CLOSE", font=("Arial", 12, "bold"),
                 command=achievements_window.destroy, bg='#e74c3c', fg='white',
                 relief=tk.FLAT, padx=30, pady=10).pack(pady=20)

    def show_shop(self):
        """Show shop in a scrollable window"""
        shop_window = tk.Toplevel(self.root)
        shop_window.title("Coin Casino Shop")
        shop_window.geometry("700x700")
        shop_window.resizable(True, True)
        shop_window.configure(bg='#0d1b2a')

        header_frame = tk.Frame(shop_window, bg='#0d1b2a')
        header_frame.pack(fill=tk.X, padx=30, pady=20)

        tk.Label(header_frame, text="🛍️", font=("Arial", 30),
                bg='#0d1b2a', fg='#ffd166').pack()
        tk.Label(header_frame, text="CASINO SHOP", font=("Arial", 20, "bold"),
                bg='#0d1b2a', fg='#e0e1dd').pack(pady=5)


        balance_frame = self.create_balance_display(header_frame)
        balance_frame.pack(pady=10)

        scrollable_shop = ScrollableFrame(shop_window, bg='#0d1b2a')
        scrollable_shop.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        container = scrollable_shop.scrollable_frame

        for key, item in self.shop_items.items():
            card = tk.Frame(container, bg='#1b263b', relief=tk.RAISED, bd=0)
            card.pack(fill=tk.X, padx=10, pady=10)

            info_frame = tk.Frame(card, bg='#1b263b')
            info_frame.pack(fill=tk.X, padx=20, pady=15)

            tk.Label(info_frame, text=item["name"], font=("Arial", 16, "bold"),
                    bg='#1b263b', fg='#e0e1dd').pack(anchor=tk.W)
            tk.Label(info_frame, text=item["description"], font=("Arial", 10),
                    bg='#1b263b', fg='#778da9').pack(anchor=tk.W)
            tk.Label(info_frame, text=f"Price: {item['price']} coins", font=("Arial", 12),
                    bg='#1b263b', fg='#ffd166').pack(anchor=tk.W, pady=(5, 0))

            action_frame = tk.Frame(card, bg='#1b263b')
            action_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

            if not item["owned"]:
                buy_btn = tk.Button(action_frame, text="BUY NOW", font=("Arial", 10, "bold"),
                                  command=lambda k=key: self.buy_item(k, shop_window),
                                  bg='#27ae60', fg='white', relief=tk.FLAT, padx=20, pady=5,
                                  cursor="hand2")
                buy_btn.pack(side=tk.RIGHT)

                def on_enter(e):
                    buy_btn['bg'] = self.lighten_color('#27ae60')
                def on_leave(e):
                    buy_btn['bg'] = '#27ae60'
                buy_btn.bind("<Enter>", on_enter)
                buy_btn.bind("<Leave>", on_leave)
            else:
                tk.Label(action_frame, text="✅ OWNED", font=("Arial", 10, "bold"),
                        bg='#1b263b', fg='#27ae60').pack(side=tk.RIGHT)

        tk.Button(shop_window, text="CLOSE", font=("Arial", 12, "bold"),
                 command=shop_window.destroy, bg='#e74c3c', fg='white',
                 relief=tk.FLAT, padx=30, pady=10, cursor="hand2").pack(pady=20)

    def buy_item(self, item_key, shop_window):
        """Purchase shop item"""
        item = self.shop_items[item_key]

        if self.balance >= item["price"]:
            self.balance -= item["price"]
            self.shop_items[item_key]["owned"] = True
            self.update_balance_display()
            self.save_profile()
            messagebox.showinfo("Purchase Successful", f"You bought {item['name']}!")
            shop_window.destroy()
            self.show_shop()
        else:
            messagebox.showerror("Purchase Failed", "Not enough coins!")

    def check_achievements(self):
        """Check and unlock achievements - now with safe access"""
        try:
            if self.stats["games_won"] >= 1 and not self.achievements.get("first_win", {}).get("unlocked", False):
                self.achievements["first_win"]["unlocked"] = True
                self.show_achievement_popup("first_win")

            if self.stats["biggest_loss"] >= 100 and not self.achievements.get("high_roller", {}).get("unlocked", False):
                self.achievements["high_roller"]["unlocked"] = True
                self.show_achievement_popup("high_roller")

            if self.balance >= 1000 and not self.achievements.get("rich", {}).get("unlocked", False):
                self.achievements["rich"]["unlocked"] = True
                self.show_achievement_popup("rich")

            if self.stats["total_games"] >= 50 and not self.achievements.get("gambler", {}).get("unlocked", False):
                self.achievements["gambler"]["unlocked"] = True
                self.show_achievement_popup("gambler")

            if self.stats["current_streak"] >= 5 and not self.achievements.get("lucky", {}).get("unlocked", False):
                self.achievements["lucky"]["unlocked"] = True
                self.show_achievement_popup("lucky")
        except Exception as e:
            print(f"Achievement check error: {e}")

    def show_achievement_popup(self, achievement_key):
        """Show achievement unlock popup"""
        achievement = self.achievements.get(achievement_key, {})
        if achievement:
            messagebox.showinfo("🎉 Achievement Unlocked!",
                              f"{achievement.get('name', 'Unknown')}\n{achievement.get('description', '')}")

    def clear_screen(self):
        """Clear all widgets from root window"""
        if self.pending_animation:
            self.root.after_cancel(self.pending_animation)
            self.pending_animation = None

        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = CoinCasino(root)
    root.mainloop()

if __name__ == "__main__":
    main()
