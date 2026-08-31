"""
TimeFlow - Native Floating Transparent Desktop Widget (Rainmeter Style)
100% Transparent background, frameless, draggable, customizable themes, mini-mode,
and Custom Target Goal Countdown (นับวันถอยหลังสู่วันเป้าหมาย).
"""

import tkinter as tk
import tkinter.messagebox as msgbox
import datetime
import json
import os
import sys

# Color Constants
TRANS_COLOR = "#000001"

THEMES = {
    "dark": {
        "name": "Midnight Glass",
        "bg": "#0f172a",
        "border": "#334155",
        "text_main": "#f8fafc",
        "text_muted": "#94a3b8",
        "track": "#1e293b",
        "year_bar": "#38bdf8",
        "month_bar": "#10b981",
        "week_bar": "#f59e0b",
        "day_bar": "#f43f5e",
        "goal_bar": "#a855f7",
        "hero_badge": "#38bdf8",
        "goal_badge": "#c084fc"
    },
    "light": {
        "name": "Clean Light",
        "bg": "#ffffff",
        "border": "#e2e8f0",
        "text_main": "#0f172a",
        "text_muted": "#64748b",
        "track": "#f1f5f9",
        "year_bar": "#2563eb",
        "month_bar": "#059669",
        "week_bar": "#d97706",
        "day_bar": "#e11d48",
        "goal_bar": "#9333ea",
        "hero_badge": "#2563eb",
        "goal_badge": "#9333ea"
    },
    "sage": {
        "name": "Sage Farm",
        "bg": "#0e2217",
        "border": "#1e4a32",
        "text_main": "#f0fdf4",
        "text_muted": "#86efac",
        "track": "#163826",
        "year_bar": "#4ade80",
        "month_bar": "#22c55e",
        "week_bar": "#facc15",
        "day_bar": "#fb7185",
        "goal_bar": "#2dd4bf",
        "hero_badge": "#4ade80",
        "goal_badge": "#2dd4bf"
    },
    "neon": {
        "name": "Neon Violet",
        "bg": "#130924",
        "border": "#3b1d6e",
        "text_main": "#faf5ff",
        "text_muted": "#c084fc",
        "track": "#241242",
        "year_bar": "#a855f7",
        "month_bar": "#06b6d4",
        "week_bar": "#f43f5e",
        "day_bar": "#eab308",
        "goal_bar": "#ec4899",
        "hero_badge": "#c084fc",
        "goal_badge": "#f472b6"
    }
}

THAI_MONTHS = [
    'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
    'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
]
THAI_DAYS = ['วันอาทิตย์', 'วันจันทร์', 'วันอังคาร', 'วันพุธ', 'วันพฤหัสบดี', 'วันศุกร์', 'วันเสาร์']

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'widget_config.json')


class TimeFlowWidget:
    def __init__(self):
        self.load_config()

        self.root = tk.Tk()
        self.root.title("TimeFlow")
        self.root.overrideredirect(True) # Frameless, no title bar
        
        # Transparent window setup for Windows
        self.root.config(bg=TRANS_COLOR)
        self.root.wm_attributes("-transparentcolor", TRANS_COLOR)
        self.root.wm_attributes("-topmost", self.is_pinned)
        self.root.wm_attributes("-alpha", 0.96)

        self.width = 360
        self.height = 560
        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        # Dragging support
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Canvas
        self.canvas = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg=TRANS_COLOR, 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.bind_events()
        self.draw_ui()
        self.update_loop()

    def load_config(self):
        self.pos_x = 100
        self.pos_y = 100
        self.theme_key = "dark"
        self.is_pinned = False
        self.is_mini = False
        self.goal_title = "เป้าหมายสำคัญ"
        self.goal_date = "2026-12-31"
        self.goal_start_date = "2026-01-01"

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.pos_x = data.get('x', 100)
                    self.pos_y = data.get('y', 100)
                    self.theme_key = data.get('theme', 'dark')
                    self.is_pinned = data.get('pinned', False)
                    self.is_mini = data.get('mini', False)
                    self.goal_title = data.get('goal_title', 'เป้าหมายสำคัญ')
                    self.goal_date = data.get('goal_date', '2026-12-31')
                    self.goal_start_date = data.get('goal_start_date', '2026-01-01')
            except Exception:
                pass

    def save_config(self):
        data = {
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y(),
            'theme': self.theme_key,
            'pinned': self.is_pinned,
            'mini': self.is_mini,
            'goal_title': self.goal_title,
            'goal_date': self.goal_date,
            'goal_start_date': self.goal_start_date
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", lambda e: self.save_config())

        # Right-click context menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🎯 ตั้งคู่วันเป้าหมาย (Set Goal Countdown)", command=self.open_goal_dialog)
        self.menu.add_separator()
        self.menu.add_command(label="📌 ตรึงลอยบนสุด (Always on Top)", command=self.toggle_pin)
        self.menu.add_command(label="➖ สลับโหมดเล็ก (Mini Mode)", command=self.toggle_mini)
        self.menu.add_separator()
        self.menu.add_command(label="🎨 ธีม: Midnight Glass", command=lambda: self.set_theme("dark"))
        self.menu.add_command(label="🎨 ธีม: Clean Light", command=lambda: self.set_theme("light"))
        self.menu.add_command(label="🎨 ธีม: Sage Farm", command=lambda: self.set_theme("sage"))
        self.menu.add_command(label="🎨 ธีม: Neon Violet", command=lambda: self.set_theme("neon"))
        self.menu.add_separator()
        self.menu.add_command(label="✕ ปิด Widget", command=self.close)

        self.canvas.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def on_drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_motion(self, event):
        deltax = event.x - self.drag_start_x
        deltay = event.y - self.drag_start_y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def round_rect(self, x1, y1, x2, y2, r=16, **kwargs):
        points = [
            x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r,
            x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2,
            x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.root.wm_attributes("-topmost", self.is_pinned)
        self.save_config()
        self.draw_ui()

    def toggle_mini(self):
        self.is_mini = not self.is_mini
        if self.is_mini:
            self.width = 340
            self.height = 68
        else:
            self.width = 360
            self.height = 560
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas.config(width=self.width, height=self.height)
        self.save_config()
        self.draw_ui()

    def set_theme(self, key):
        self.theme_key = key
        self.save_config()
        self.draw_ui()

    def next_theme(self):
        keys = list(THEMES.keys())
        idx = keys.index(self.theme_key)
        self.set_theme(keys[(idx + 1) % len(keys)])

    def close(self):
        self.save_config()
        self.root.destroy()

    def open_goal_dialog(self):
        # Modern Modal Dialog for Goal Settings
        dialog = tk.Toplevel(self.root)
        dialog.title("ตั้งคู่วันเป้าหมาย 🎯")
        dialog.geometry("320x240")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        t = THEMES[self.theme_key]
        dialog.config(bg=t["bg"])

        # Title Label & Entry
        lbl_title = tk.Label(dialog, text="ชื่อเป้าหมาย / กิจกรรม:", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 9, "bold"))
        lbl_title.pack(anchor="w", padx=20, pady=(16, 4))

        entry_title = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["track"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_title.insert(0, self.goal_title)
        entry_title.pack(fill="x", padx=20, pady=(0, 12), ipady=4)

        # Date Label & Entry
        lbl_date = tk.Label(dialog, text="วันเป้าหมาย (YYYY-MM-DD เช่น 2026-12-31):", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 9, "bold"))
        lbl_date.pack(anchor="w", padx=20, pady=(0, 4))

        entry_date = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["track"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_date.insert(0, self.goal_date)
        entry_date.pack(fill="x", padx=20, pady=(0, 16), ipady=4)

        # Save Button
        def on_save():
            new_title = entry_title.get().strip() or "เป้าหมายสำคัญ"
            new_date_str = entry_date.get().strip()

            try:
                # Validate date format
                datetime.date.fromisoformat(new_date_str)
                self.goal_title = new_title
                self.goal_date = new_date_str
                self.goal_start_date = datetime.date.today().isoformat()
                self.save_config()
                self.draw_ui()
                dialog.destroy()
            except ValueError:
                msgbox.showerror("รูปแบบวันที่ไม่ถูกต้อง", "กรุณาใส่วันที่ในรูปแบบ ปี-เดือน-วัน\nเช่น 2026-12-31 หรือ 2026-10-15", parent=dialog)

        btn_save = tk.Button(dialog, text="บันทึกเป้าหมาย 💾", bg=t["goal_bar"], fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", command=on_save, cursor="hand2")
        btn_save.pack(fill="x", padx=20, ipady=5)

    def calculate_progress(self):
        now = datetime.datetime.now()
        year = now.year

        # Year %
        year_start = datetime.datetime(year, 1, 1)
        year_end = datetime.datetime(year + 1, 1, 1)
        year_pct = ((now - year_start) / (year_end - year_start)) * 100
        year_days_left = (year_end.date() - now.date()).days

        # Month %
        month = now.month
        month_start = datetime.datetime(year, month, 1)
        next_month_start = datetime.datetime(year + 1, 1, 1) if month == 12 else datetime.datetime(year, month + 1, 1)
        month_pct = ((now - month_start) / (next_month_start - month_start)) * 100
        month_days_left = (next_month_start.date() - now.date()).days

        # Week %
        weekday = now.weekday() # 0 = Mon, 6 = Sun
        week_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=weekday)
        week_end = week_start + datetime.timedelta(days=7)
        week_pct = ((now - week_start) / (week_end - week_start)) * 100
        week_days_left = 6 - weekday

        # Day %
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + datetime.timedelta(days=1)
        day_pct = ((now - day_start) / (day_end - day_start)) * 100
        day_rem = day_end - now
        day_hours = day_rem.seconds // 3600
        day_mins = (day_rem.seconds % 3600) // 60

        # Custom Goal Milestone Countdown
        today_date = now.date()
        try:
            target_d = datetime.date.fromisoformat(self.goal_date)
            goal_days_left = (target_d - today_date).days
            
            try:
                start_d = datetime.date.fromisoformat(self.goal_start_date)
            except Exception:
                start_d = today_date

            total_goal_days = (target_d - start_d).days
            passed_goal_days = (today_date - start_d).days
            if total_goal_days > 0:
                goal_pct = max(0.0, min(100.0, (passed_goal_days / total_goal_days) * 100))
            else:
                goal_pct = 100.0 if goal_days_left <= 0 else 0.0
        except Exception:
            goal_days_left = 0
            goal_pct = 0.0

        if goal_days_left > 0:
            goal_badge = f"D-{goal_days_left} วัน"
            goal_sub = f"เป้าหมาย: {self.goal_date} (เหลืออีก {goal_days_left} วัน)"
        elif goal_days_left == 0:
            goal_badge = "D-Day! 🎉"
            goal_sub = "วันนี้คือวันเป้าหมายของคุณแล้ว! ลุยเลย!"
        else:
            goal_badge = f"D+{abs(goal_days_left)} วัน"
            goal_sub = f"ผ่านวันเป้าหมายมาแล้ว {abs(goal_days_left)} วัน"

        return {
            "now": now,
            "year": year,
            "year_pct": year_pct,
            "year_days_left": year_days_left,
            "month_name": THAI_MONTHS[month - 1],
            "month_pct": month_pct,
            "month_days_left": month_days_left,
            "week_pct": week_pct,
            "week_days_left": week_days_left,
            "day_pct": day_pct,
            "day_hours": day_hours,
            "day_mins": day_mins,
            "goal_title": self.goal_title,
            "goal_badge": goal_badge,
            "goal_days_left": goal_days_left,
            "goal_pct": goal_pct,
            "goal_sub": goal_sub,
            "time_str": now.strftime("%H:%M:%S"),
            "date_str": f"{THAI_DAYS[now.isoweekday() % 7]}ที่ {now.day} {THAI_MONTHS[month - 1]} {year}"
        }

    def draw_ui(self):
        self.canvas.delete("all")
        t = THEMES[self.theme_key]
        data = self.calculate_progress()

        if self.is_mini:
            # -------------------------------------------------------------
            # MINI CAPSULE VIEW
            # -------------------------------------------------------------
            self.round_rect(4, 4, self.width - 4, self.height - 4, r=18, fill=t["bg"], outline=t["border"], width=1.2)
            
            # Left icon & goal or year text
            self.canvas.create_text(20, self.height // 2, text="🎯", font=("Segoe UI Emoji", 12), anchor="w")
            self.canvas.create_text(42, self.height // 2, text=f"{data['goal_title'][:10]}:", font=("Segoe UI", 9, "bold"), fill=t["text_main"], anchor="w")
            
            # Bar
            bx1, by1, bx2, by2 = 135, (self.height // 2) - 4, 235, (self.height // 2) + 4
            self.round_rect(bx1, by1, bx2, by2, r=4, fill=t["track"])
            fill_w = bx1 + (bx2 - bx1) * (data['goal_pct'] / 100)
            if fill_w > bx1 + 4:
                self.round_rect(bx1, by1, fill_w, by2, r=4, fill=t["goal_bar"])

            # Badge (e.g. D-45)
            self.canvas.create_text(245, self.height // 2, text=data['goal_badge'], font=("Segoe UI", 9, "bold"), fill=t["goal_badge"], anchor="w")
            
            # Expand btn
            btn_exp = self.canvas.create_text(self.width - 20, self.height // 2, text="➕", font=("Segoe UI", 11), fill=t["text_muted"])
            self.canvas.tag_bind(btn_exp, "<Button-1>", lambda e: self.toggle_mini())
            return

        # -----------------------------------------------------------------
        # FULL CARD VIEW
        # -----------------------------------------------------------------
        # Outer Card Background (Rounded with subtle border)
        self.round_rect(5, 5, self.width - 5, self.height - 5, r=22, fill=t["bg"], outline=t["border"], width=1.5)

        # Header Bar
        self.canvas.create_text(26, 28, text="⏳", font=("Segoe UI Emoji", 13), anchor="w")
        self.canvas.create_text(48, 28, text="TimeFlow", font=("Segoe UI", 11, "bold"), fill=t["text_main"], anchor="w")

        # Goal Edit Button
        btn_goal_set = self.canvas.create_text(self.width - 122, 28, text="🎯", font=("Segoe UI Emoji", 10), fill=t["text_muted"])
        self.canvas.tag_bind(btn_goal_set, "<Button-1>", lambda e: self.open_goal_dialog())

        # Pin button
        pin_color = "#38bdf8" if self.is_pinned else t["text_muted"]
        btn_pin = self.canvas.create_text(self.width - 98, 28, text="📌", font=("Segoe UI Emoji", 10), fill=pin_color)
        self.canvas.tag_bind(btn_pin, "<Button-1>", lambda e: self.toggle_pin())

        # Mini button
        btn_mini = self.canvas.create_text(self.width - 74, 28, text="➖", font=("Segoe UI", 11), fill=t["text_muted"])
        self.canvas.tag_bind(btn_mini, "<Button-1>", lambda e: self.toggle_mini())

        # Theme button
        btn_th = self.canvas.create_text(self.width - 50, 28, text="🎨", font=("Segoe UI Emoji", 10), fill=t["text_muted"])
        self.canvas.tag_bind(btn_th, "<Button-1>", lambda e: self.next_theme())

        # Close button
        btn_cl = self.canvas.create_text(self.width - 26, 28, text="✕", font=("Segoe UI", 11), fill=t["text_muted"])
        self.canvas.tag_bind(btn_cl, "<Button-1>", lambda e: self.close())

        # 1. Live Clock & Date
        self.time_label_id = self.canvas.create_text(self.width // 2, 70, text=data["time_str"], font=("Segoe UI", 25, "bold"), fill=t["text_main"])
        self.date_label_id = self.canvas.create_text(self.width // 2, 98, text=data["date_str"], font=("Segoe UI", 9), fill=t["text_muted"])

        # Progress Tracks Container
        # 1. Goal Milestone Countdown Card (Interactive Click to Edit)
        self.draw_goal_card(
            y=120,
            height=66,
            data=data,
            theme=t
        )

        # 2. Year Progress
        self.draw_progress_item(
            y=194, 
            height=64,
            emoji="🌍", 
            title=f"ปี {data['year']}", 
            pct=data['year_pct'], 
            badge_text=f"{data['year_pct']:.1f}%",
            sub_text=f"เหลืออีก {data['year_days_left']} วันในปีนี้",
            bar_color=t["year_bar"],
            is_hero=True,
            theme=t
        )

        # 3. Month Progress
        self.draw_progress_item(
            y=266, 
            height=56,
            emoji="🗓️", 
            title=data['month_name'], 
            pct=data['month_pct'], 
            badge_text=f"{data['month_pct']:.1f}%",
            sub_text=f"เหลืออีก {data['month_days_left']} วันในเดือนนี้",
            bar_color=t["month_bar"],
            is_hero=False,
            theme=t
        )

        # 4. Week Progress
        self.draw_progress_item(
            y=330, 
            height=56,
            emoji="📅", 
            title="สัปดาห์นี้", 
            pct=data['week_pct'], 
            badge_text=f"{data['week_pct']:.1f}%",
            sub_text=f"เหลืออีก {data['week_days_left']} วันในสัปดาห์นี้",
            bar_color=t["week_bar"],
            is_hero=False,
            theme=t
        )

        # 5. Today Progress
        self.draw_progress_item(
            y=394, 
            height=56,
            emoji="☀️", 
            title="วันนี้ (Today)", 
            pct=data['day_pct'], 
            badge_text=f"{data['day_pct']:.1f}%",
            sub_text=f"เหลืออีก {data['day_hours']} ชม. {data['day_mins']} นาที",
            bar_color=t["day_bar"],
            is_hero=False,
            theme=t
        )

        # Footer Quote / Mindfulness
        self.round_rect(18, 464, self.width - 18, 542, r=10, fill=t["track"], outline=t["border"], width=1)
        self.canvas.create_text(30, 485, text="💭", font=("Segoe UI Emoji", 10), anchor="w")
        self.canvas.create_text(48, 485, text="เวลาคือสิ่งเดียวที่ผ่านไปแล้วไม่ย้อนกลับ ✨", font=("Segoe UI", 8), fill=t["text_muted"], anchor="w")
        self.canvas.create_text(48, 520, text="คลิกที่การ์ด 🎯 เพื่อเปลี่ยนวันเป้าหมาย", font=("Segoe UI", 7, "italic"), fill=t["text_muted"], anchor="w")

    def draw_goal_card(self, y, height, data, theme):
        x1 = 18
        x2 = self.width - 18
        y1 = y
        y2 = y + height

        # Highlighted Goal Card Container (Click to edit)
        card_id = self.round_rect(x1, y1, x2, y2, r=14, fill=theme["track"], outline=theme["goal_bar"], width=1.4)
        self.canvas.tag_bind(card_id, "<Button-1>", lambda e: self.open_goal_dialog())

        # Title
        t_id1 = self.canvas.create_text(x1 + 12, y1 + 16, text="🎯", font=("Segoe UI Emoji", 11), anchor="w")
        t_id2 = self.canvas.create_text(x1 + 32, y1 + 16, text=data["goal_title"], font=("Segoe UI", 9, "bold"), fill=theme["text_main"], anchor="w")

        # Badge D-XX
        t_id3 = self.canvas.create_text(x2 - 12, y1 + 16, text=data["goal_badge"], font=("Segoe UI", 10, "bold"), fill=theme["goal_badge"], anchor="e")

        # Progress bar towards goal
        bar_x1 = x1 + 12
        bar_x2 = x2 - 12
        bar_y1 = y1 + 30
        bar_h = 6
        bar_y2 = bar_y1 + bar_h

        self.round_rect(bar_x1, bar_y1, bar_x2, bar_y2, r=3, fill="#0b1120" if theme == THEMES["dark"] else "#cbd5e1")
        fill_width = bar_x1 + (bar_x2 - bar_x1) * (data['goal_pct'] / 100.0)
        if fill_width > bar_x1 + 3:
            self.round_rect(bar_x1, bar_y1, fill_width, bar_y2, r=3, fill=theme["goal_bar"])

        # Sub text
        t_id4 = self.canvas.create_text(x1 + 12, y1 + 48, text=data["goal_sub"], font=("Segoe UI", 8), fill=theme["text_muted"], anchor="w")

        # Bind all text elements to open dialog
        for elem in [t_id1, t_id2, t_id3, t_id4]:
            self.canvas.tag_bind(elem, "<Button-1>", lambda e: self.open_goal_dialog())

    def draw_progress_item(self, y, height, emoji, title, pct, badge_text, sub_text, bar_color, is_hero, theme):
        x1 = 18
        x2 = self.width - 18
        y1 = y
        y2 = y + height

        # Card block
        self.round_rect(x1, y1, x2, y2, r=12, fill=theme["track"], outline=theme["border"], width=1)

        # Title & Pct
        self.canvas.create_text(x1 + 12, y1 + 15, text=emoji, font=("Segoe UI Emoji", 10), anchor="w")
        title_font = ("Segoe UI", 9, "bold") if is_hero else ("Segoe UI", 8, "bold")
        self.canvas.create_text(x1 + 30, y1 + 15, text=title, font=title_font, fill=theme["text_main"], anchor="w")

        pct_font = ("Segoe UI", 10, "bold") if is_hero else ("Segoe UI", 8, "bold")
        pct_color = theme["hero_badge"] if is_hero else theme["text_main"]
        self.canvas.create_text(x2 - 12, y1 + 15, text=badge_text, font=pct_font, fill=pct_color, anchor="e")

        # Progress bar
        bar_x1 = x1 + 12
        bar_x2 = x2 - 12
        bar_y1 = y1 + 28
        bar_h = 7 if is_hero else 5
        bar_y2 = bar_y1 + bar_h

        # Track
        self.round_rect(bar_x1, bar_y1, bar_x2, bar_y2, r=bar_h // 2, fill="#0b1120" if theme == THEMES["dark"] else "#cbd5e1")
        
        # Fill
        fill_width = bar_x1 + (bar_x2 - bar_x1) * (pct / 100.0)
        if fill_width > bar_x1 + 3:
            self.round_rect(bar_x1, bar_y1, fill_width, bar_y2, r=bar_h // 2, fill=bar_color)

        # Sub text
        self.canvas.create_text(x1 + 12, y1 + 44 + (1 if is_hero else 0), text=sub_text, font=("Segoe UI", 7), fill=theme["text_muted"], anchor="w")

    def update_loop(self):
        if hasattr(self, 'time_label_id') and not self.is_mini:
            data = self.calculate_progress()
            self.canvas.itemconfig(self.time_label_id, text=data["time_str"])
            self.canvas.itemconfig(self.date_label_id, text=data["date_str"])
        
        # Redraw full UI every minute to update progress bars
        now = datetime.datetime.now()
        if now.second == 0:
            self.draw_ui()

        self.root.after(1000, self.update_loop)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TimeFlowWidget()
    app.run()
