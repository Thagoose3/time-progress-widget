"""
TimeFlow - Ultra-Minimalist & Crystal-Clear Floating Desktop Widget
Features High-DPI crisp rendering, transparent borderless glassmorphism,
unified breathable layout, and interactive custom goal countdown.
"""

import ctypes
import datetime
import json
import os
import sys
import tkinter as tk
import tkinter.messagebox as msgbox

# Enable Windows High-DPI Awareness for Crystal-Clear Text & Crisp Rendering
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # Per-monitor DPI aware
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

TRANS_COLOR = "#000001"

THEMES = {
    "dark": {
        "name": "Obsidian Minimal",
        "bg": "#090d16",
        "card_bg": "#121826",
        "border": "#1e293b",
        "border_subtle": "#172033",
        "text_main": "#f8fafc",
        "text_muted": "#818cf8",
        "text_sub": "#64748b",
        "track": "#1e293b",
        "year_bar": "#38bdf8",
        "month_bar": "#34d399",
        "week_bar": "#fbbf24",
        "day_bar": "#f43f5e",
        "goal_bar": "#a855f7",
        "goal_glow": "#c084fc",
        "accent": "#38bdf8"
    },
    "light": {
        "name": "Pure White",
        "bg": "#ffffff",
        "card_bg": "#f8fafc",
        "border": "#e2e8f0",
        "border_subtle": "#f1f5f9",
        "text_main": "#0f172a",
        "text_muted": "#4f46e5",
        "text_sub": "#94a3b8",
        "track": "#e2e8f0",
        "year_bar": "#0284c7",
        "month_bar": "#059669",
        "week_bar": "#d97706",
        "day_bar": "#e11d48",
        "goal_bar": "#7c3aed",
        "goal_glow": "#7c3aed",
        "accent": "#0284c7"
    },
    "sage": {
        "name": "Sage Minimal",
        "bg": "#0a1811",
        "card_bg": "#11261b",
        "border": "#1d402e",
        "border_subtle": "#163324",
        "text_main": "#f0fdf4",
        "text_muted": "#86efac",
        "text_sub": "#4ade80",
        "track": "#1b3a2a",
        "year_bar": "#4ade80",
        "month_bar": "#22c55e",
        "week_bar": "#facc15",
        "day_bar": "#fb7185",
        "goal_bar": "#2dd4bf",
        "goal_glow": "#5eead4",
        "accent": "#4ade80"
    },
    "neon": {
        "name": "Cyber Midnight",
        "bg": "#0c0717",
        "card_bg": "#170e2c",
        "border": "#2e1854",
        "border_subtle": "#221140",
        "text_main": "#faf5ff",
        "text_muted": "#c084fc",
        "text_sub": "#818cf8",
        "track": "#271448",
        "year_bar": "#c084fc",
        "month_bar": "#22d3ee",
        "week_bar": "#f472b6",
        "day_bar": "#fbbf24",
        "goal_bar": "#f43f5e",
        "goal_glow": "#fb7185",
        "accent": "#c084fc"
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
        self.root.overrideredirect(True) # Borderless & Frameless
        
        # Transparency settings
        self.root.config(bg=TRANS_COLOR)
        self.root.wm_attributes("-transparentcolor", TRANS_COLOR)
        self.root.wm_attributes("-topmost", self.is_pinned)
        self.root.wm_attributes("-alpha", 0.98)

        # Dimensions: Clean, sleek, non-cluttered
        self.width = 340
        self.height = 540
        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        # Dragging coordinates
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
        self.goal_title = "วันรับปริญญา"
        self.goal_date = "2026-12-24"
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
                    self.goal_title = data.get('goal_title', 'วันรับปริญญา')
                    self.goal_date = data.get('goal_date', '2026-12-24')
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

        # Context Menu
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="🎯 ตั้งคู่วันเป้าหมาย (Set Target Goal)", command=self.open_goal_dialog)
        self.menu.add_separator()
        self.menu.add_command(label="📌 ตรึงลอยบนสุด (Always on Top)", command=self.toggle_pin)
        self.menu.add_command(label="➖ สลับโหมดแคปซูลเล็ก (Mini Mode)", command=self.toggle_mini)
        self.menu.add_separator()
        self.menu.add_command(label="🎨 ธีม: Obsidian Minimal", command=lambda: self.set_theme("dark"))
        self.menu.add_command(label="🎨 ธีม: Pure White", command=lambda: self.set_theme("light"))
        self.menu.add_command(label="🎨 ธีม: Sage Minimal", command=lambda: self.set_theme("sage"))
        self.menu.add_command(label="🎨 ธีม: Cyber Midnight", command=lambda: self.set_theme("neon"))
        self.menu.add_separator()
        self.menu.add_command(label="✕ ปิด Widget", command=self.close)

        self.canvas.bind("<Button-3>", lambda event: self.menu.tk_popup(event.x_root, event.y_root))

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
            self.width = 320
            self.height = 58
        else:
            self.width = 340
            self.height = 540
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
        dialog = tk.Toplevel(self.root)
        dialog.title("ตั้งคู่วันเป้าหมาย 🎯")
        dialog.geometry("320x220")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        t = THEMES[self.theme_key]
        dialog.config(bg=t["bg"])

        lbl_title = tk.Label(dialog, text="ชื่อเป้าหมาย / กิจกรรม:", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 9, "bold"))
        lbl_title.pack(anchor="w", padx=22, pady=(16, 4))

        entry_title = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["card_bg"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_title.insert(0, self.goal_title)
        entry_title.pack(fill="x", padx=22, pady=(0, 10), ipady=4)

        lbl_date = tk.Label(dialog, text="วันเป้าหมาย (YYYY-MM-DD เช่น 2026-12-24):", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 9, "bold"))
        lbl_date.pack(anchor="w", padx=22, pady=(0, 4))

        entry_date = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["card_bg"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_date.insert(0, self.goal_date)
        entry_date.pack(fill="x", padx=22, pady=(0, 16), ipady=4)

        def on_save():
            new_title = entry_title.get().strip() or "เป้าหมายสำคัญ"
            new_date_str = entry_date.get().strip()
            try:
                datetime.date.fromisoformat(new_date_str)
                self.goal_title = new_title
                self.goal_date = new_date_str
                self.goal_start_date = datetime.date.today().isoformat()
                self.save_config()
                self.draw_ui()
                dialog.destroy()
            except ValueError:
                msgbox.showerror("รูปแบบวันที่ไม่ถูกต้อง", "กรุณาใส่วันที่ในรูปแบบ ปี-เดือน-วัน\nเช่น 2026-12-24", parent=dialog)

        btn_save = tk.Button(dialog, text="บันทึกเป้าหมาย 💾", bg=t["goal_bar"], fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", command=on_save, cursor="hand2")
        btn_save.pack(fill="x", padx=22, ipady=4)

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

        # Target Goal Milestone
        today_date = now.date()
        try:
            target_d = datetime.date.fromisoformat(self.goal_date)
            goal_days_left = (target_d - today_date).days
            
            try:
                start_d = datetime.date.fromisoformat(self.goal_start_date)
            except Exception:
                start_d = today_date

            total_days = (target_d - start_d).days
            passed_days = (today_date - start_d).days
            if total_days > 0:
                goal_pct = max(0.0, min(100.0, (passed_days / total_days) * 100))
            else:
                goal_pct = 100.0 if goal_days_left <= 0 else 0.0
        except Exception:
            goal_days_left = 0
            goal_pct = 0.0

        if goal_days_left > 0:
            goal_badge = f"D-{goal_days_left} วัน"
            goal_sub = f"เหลืออีก {goal_days_left} วัน ({self.goal_date})"
        elif goal_days_left == 0:
            goal_badge = "D-Day! 🎉"
            goal_sub = "วันนี้คือวันเป้าหมายของคุณ!"
        else:
            goal_badge = f"D+{abs(goal_days_left)} วัน"
            goal_sub = f"ผ่านวันเป้าหมายมา {abs(goal_days_left)} วัน"

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
            # MINI CAPSULE VIEW (Clean & Minimal)
            # -------------------------------------------------------------
            self.round_rect(4, 4, self.width - 4, self.height - 4, r=16, fill=t["bg"], outline=t["border"], width=1.2)
            
            # Left icon & goal
            self.canvas.create_text(18, self.height // 2, text="🎯", font=("Segoe UI Emoji", 11), anchor="w")
            self.canvas.create_text(38, self.height // 2, text=f"{data['goal_title'][:9]}:", font=("Segoe UI", 9, "bold"), fill=t["text_main"], anchor="w")
            
            # Bar
            bx1, by1, bx2, by2 = 120, (self.height // 2) - 3, 220, (self.height // 2) + 3
            self.round_rect(bx1, by1, bx2, by2, r=3, fill=t["track"])
            fill_w = bx1 + (bx2 - bx1) * (data['goal_pct'] / 100)
            if fill_w > bx1 + 3:
                self.round_rect(bx1, by1, fill_w, by2, r=3, fill=t["goal_bar"])

            # Badge
            self.canvas.create_text(230, self.height // 2, text=data['goal_badge'], font=("Segoe UI", 9, "bold"), fill=t["goal_glow"], anchor="w")
            
            # Expand btn
            btn_exp = self.canvas.create_text(self.width - 18, self.height // 2, text="➕", font=("Segoe UI", 10), fill=t["text_sub"])
            self.canvas.tag_bind(btn_exp, "<Button-1>", lambda e: self.toggle_mini())
            return

        # -----------------------------------------------------------------
        # FULL CARD VIEW (Clean, Breathable, Minimalist)
        # -----------------------------------------------------------------
        # Outer Card
        self.round_rect(5, 5, self.width - 5, self.height - 5, r=24, fill=t["bg"], outline=t["border"], width=1.5)

        # Header Bar: Brand + Clean Action Icons
        self.canvas.create_text(24, 26, text="⏳", font=("Segoe UI Emoji", 12), anchor="w")
        self.canvas.create_text(46, 26, text="TimeFlow", font=("Segoe UI", 11, "bold"), fill=t["text_main"], anchor="w")

        # Subtle Header Action Icons
        pin_color = t["accent"] if self.is_pinned else t["text_sub"]
        btn_pin = self.canvas.create_text(self.width - 92, 26, text="📌", font=("Segoe UI Emoji", 9), fill=pin_color)
        self.canvas.tag_bind(btn_pin, "<Button-1>", lambda e: self.toggle_pin())

        btn_mini = self.canvas.create_text(self.width - 68, 26, text="➖", font=("Segoe UI", 10), fill=t["text_sub"])
        self.canvas.tag_bind(btn_mini, "<Button-1>", lambda e: self.toggle_mini())

        btn_th = self.canvas.create_text(self.width - 46, 26, text="🎨", font=("Segoe UI Emoji", 9), fill=t["text_sub"])
        self.canvas.tag_bind(btn_th, "<Button-1>", lambda e: self.next_theme())

        btn_cl = self.canvas.create_text(self.width - 24, 26, text="✕", font=("Segoe UI", 10), fill=t["text_sub"])
        self.canvas.tag_bind(btn_cl, "<Button-1>", lambda e: self.close())

        # 1. Hero Digital Clock & Date
        self.time_label_id = self.canvas.create_text(self.width // 2, 64, text=data["time_str"], font=("Segoe UI", 26, "bold"), fill=t["text_main"])
        self.date_label_id = self.canvas.create_text(self.width // 2, 92, text=data["date_str"], font=("Segoe UI", 9), fill=t["text_sub"])

        # 2. Sleek Highlight Goal Card
        self.draw_goal_card(y=114, data=data, theme=t)

        # 3. Unified Time Progress Rows (No Clunky Nested Boxes)
        self.draw_progress_row(y=190, emoji="🌍", title=f"ปี {data['year']}", pct=data['year_pct'], sub=f"เหลืออีก {data['year_days_left']} วัน", bar_color=t["year_bar"], theme=t)
        self.draw_progress_row(y=255, emoji="🗓️", title=data['month_name'], pct=data['month_pct'], sub=f"เหลืออีก {data['month_days_left']} วัน", bar_color=t["month_bar"], theme=t)
        self.draw_progress_row(y=320, emoji="📅", title="สัปดาห์นี้", pct=data['week_pct'], sub=f"เหลืออีก {data['week_days_left']} วัน", bar_color=t["week_bar"], theme=t)
        self.draw_progress_row(y=385, emoji="☀️", title="วันนี้ (Today)", pct=data['day_pct'], sub=f"เหลืออีก {data['day_hours']} ชม. {data['day_mins']} นาที", bar_color=t["day_bar"], theme=t)

        # 4. Subtle Minimal Footer Quote
        quote_y = 485
        self.canvas.create_text(self.width // 2, quote_y, text="เวลาคือสิ่งเดียวที่ผ่านไปแล้วไม่ย้อนกลับ ✨", font=("Segoe UI", 8), fill=t["text_sub"])
        self.canvas.create_text(self.width // 2, quote_y + 20, text="(คลิกที่การ์ดเป้าหมายเพื่อแก้ไข)", font=("Segoe UI", 7), fill=t["text_sub"])

    def draw_goal_card(self, y, data, theme):
        x1 = 18
        x2 = self.width - 18
        y1 = y
        y2 = y + 62

        # Sleek Card Background (Clickable)
        card_id = self.round_rect(x1, y1, x2, y2, r=14, fill=theme["card_bg"], outline=theme["goal_bar"], width=1.2)
        self.canvas.tag_bind(card_id, "<Button-1>", lambda e: self.open_goal_dialog())

        # Title & Badge
        t1 = self.canvas.create_text(x1 + 12, y1 + 15, text="🎯", font=("Segoe UI Emoji", 10), anchor="w")
        t2 = self.canvas.create_text(x1 + 30, y1 + 15, text=data["goal_title"], font=("Segoe UI", 9, "bold"), fill=theme["text_main"], anchor="w")
        t3 = self.canvas.create_text(x2 - 12, y1 + 15, text=data["goal_badge"], font=("Segoe UI", 9, "bold"), fill=theme["goal_glow"], anchor="e")

        # Progress bar
        bx1 = x1 + 12
        bx2 = x2 - 12
        by1 = y1 + 28
        by2 = by1 + 5

        self.round_rect(bx1, by1, bx2, by2, r=2.5, fill=theme["track"])
        fill_w = bx1 + (bx2 - bx1) * (data['goal_pct'] / 100.0)
        if fill_w > bx1 + 2:
            self.round_rect(bx1, by1, fill_w, by2, r=2.5, fill=theme["goal_bar"])

        # Subtext
        t4 = self.canvas.create_text(x1 + 12, y1 + 46, text=data["goal_sub"], font=("Segoe UI", 7), fill=theme["text_sub"], anchor="w")

        for el in [t1, t2, t3, t4]:
            self.canvas.tag_bind(el, "<Button-1>", lambda e: self.open_goal_dialog())

    def draw_progress_row(self, y, emoji, title, pct, sub, bar_color, theme):
        x1 = 20
        x2 = self.width - 20

        # Row 1: Label on left, Pct on right
        self.canvas.create_text(x1, y, text=emoji, font=("Segoe UI Emoji", 10), anchor="w")
        self.canvas.create_text(x1 + 20, y, text=title, font=("Segoe UI", 9, "bold"), fill=theme["text_main"], anchor="w")
        self.canvas.create_text(x2, y, text=f"{pct:.1f}%", font=("Segoe UI", 9, "bold"), fill=theme["text_main"], anchor="e")

        # Row 2: Smooth Progress Bar
        bx1 = x1
        bx2 = x2
        by1 = y + 14
        by2 = by1 + 6

        self.round_rect(bx1, by1, bx2, by2, r=3, fill=theme["track"])
        fill_w = bx1 + (bx2 - bx1) * (pct / 100.0)
        if fill_w > bx1 + 2:
            self.round_rect(bx1, by1, fill_w, by2, r=3, fill=bar_color)

        # Row 3: Subtitle
        self.canvas.create_text(x1, y + 30, text=sub, font=("Segoe UI", 7), fill=theme["text_sub"], anchor="w")

    def update_loop(self):
        if hasattr(self, 'time_label_id') and not self.is_mini:
            data = self.calculate_progress()
            self.canvas.itemconfig(self.time_label_id, text=data["time_str"])
            self.canvas.itemconfig(self.date_label_id, text=data["date_str"])
        
        now = datetime.datetime.now()
        if now.second == 0:
            self.draw_ui()

        self.root.after(1000, self.update_loop)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TimeFlowWidget()
    app.run()
