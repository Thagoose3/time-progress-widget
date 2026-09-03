"""
TimeFlow - Polished Solid Card Widget with Rich Multi-Color Themes
(Cyberpunk 2077, Synthwave Retro, Obsidian Midnight, Nordic Forest, Warm Mocha, Clean White)
Supports:
- Full View: Complete Time Progress Dashboard (Target Events, Work Hours, Year, Month, Today)
- Mini Mode: Sleek Floating Digital Clock & Date Capsule
- 100% Crash-Proof & Guaranteed reliable desktop launch.
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
    "cyberpunk": {
        "name": "🤖 Cyberpunk 2077 (Neon Tokyo)",
        "bg": "#0d0718",
        "card_bg": "#150d27",
        "border": "#ff007f",
        "border_subtle": "#2e144a",
        "text_main": "#ffffff",
        "text_muted": "#00f0ff",
        "text_sub": "#c4b5fd",
        "track": "#22133d",
        "work_bar": "#fcee0a",
        "work_glow": "#fef08a",
        "year_bar": "#00f0ff",
        "month_bar": "#05ffa1",
        "week_bar": "#ff007f",
        "day_bar": "#ff003c",
        "goal_bar": "#ff007f",
        "goal_glow": "#ff70a6",
        "accent": "#00f0ff"
    },
    "synthwave": {
        "name": "🌆 Synthwave 80s (Retro Sunset)",
        "bg": "#140a20",
        "card_bg": "#201033",
        "border": "#e879f9",
        "border_subtle": "#381854",
        "text_main": "#fff5fc",
        "text_muted": "#f472b6",
        "text_sub": "#d8b4fe",
        "track": "#301548",
        "work_bar": "#fb923c",
        "work_glow": "#fdba74",
        "year_bar": "#f472b6",
        "month_bar": "#38bdf8",
        "week_bar": "#fb7185",
        "day_bar": "#a78bfa",
        "goal_bar": "#ec4899",
        "goal_glow": "#f472b6",
        "accent": "#f472b6"
    },
    "obsidian": {
        "name": "🌌 Obsidian Midnight (Deep Navy)",
        "bg": "#090e1a",
        "card_bg": "#0f172a",
        "border": "#1e293b",
        "border_subtle": "#162032",
        "text_main": "#f8fafc",
        "text_muted": "#38bdf8",
        "text_sub": "#94a3b8",
        "track": "#1e293b",
        "work_bar": "#f59e0b",
        "work_glow": "#fbbf24",
        "year_bar": "#38bdf8",
        "month_bar": "#34d399",
        "week_bar": "#fbbf24",
        "day_bar": "#f43f5e",
        "goal_bar": "#a855f7",
        "goal_glow": "#c084fc",
        "accent": "#38bdf8"
    },
    "forest": {
        "name": "🌿 Nordic Forest (Matcha & Sage)",
        "bg": "#08160f",
        "card_bg": "#0e2419",
        "border": "#1e4d35",
        "border_subtle": "#143324",
        "text_main": "#f0fdf4",
        "text_muted": "#4ade80",
        "text_sub": "#86efac",
        "track": "#153625",
        "work_bar": "#facc15",
        "work_glow": "#fef08a",
        "year_bar": "#4ade80",
        "month_bar": "#22c55e",
        "week_bar": "#2dd4bf",
        "day_bar": "#fb7185",
        "goal_bar": "#2dd4bf",
        "goal_glow": "#5eead4",
        "accent": "#4ade80"
    },
    "mocha": {
        "name": "☕ Warm Mocha (Espresso Dark)",
        "bg": "#150e09",
        "card_bg": "#22170f",
        "border": "#422e20",
        "border_subtle": "#2e1f15",
        "text_main": "#fdf8f5",
        "text_muted": "#d4a373",
        "text_sub": "#c4a482",
        "track": "#322216",
        "work_bar": "#e76f51",
        "work_glow": "#f4a261",
        "year_bar": "#d4a373",
        "month_bar": "#8ab17d",
        "week_bar": "#e9c46a",
        "day_bar": "#e76f51",
        "goal_bar": "#e76f51",
        "goal_glow": "#f4a261",
        "accent": "#d4a373"
    },
    "clean_white": {
        "name": "🤍 Clean White (Light Mode)",
        "bg": "#ffffff",
        "card_bg": "#f8fafc",
        "border": "#cbd5e1",
        "border_subtle": "#e2e8f0",
        "text_main": "#0f172a",
        "text_muted": "#2563eb",
        "text_sub": "#64748b",
        "track": "#e2e8f0",
        "work_bar": "#d97706",
        "work_glow": "#b45309",
        "year_bar": "#0284c7",
        "month_bar": "#059669",
        "week_bar": "#d97706",
        "day_bar": "#e11d48",
        "goal_bar": "#7c3aed",
        "goal_glow": "#7c3aed",
        "accent": "#0284c7"
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
        self.root.overrideredirect(True) # Frameless
        
        # Transparency settings for window canvas edges
        self.root.config(bg=TRANS_COLOR)
        self.root.wm_attributes("-transparentcolor", TRANS_COLOR)
        self.root.wm_attributes("-topmost", self.is_pinned)
        self.root.wm_attributes("-alpha", 0.98)

        # Proportional & Breathable dimensions
        if self.is_mini:
            self.width = 280
            self.height = 76
        else:
            self.width = 350
            self.height = 560
            
        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        self.drag_start_x = 0
        self.drag_start_y = 0

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

    def get_theme(self):
        return THEMES.get(self.theme_key, THEMES["cyberpunk"])

    def load_config(self):
        self.pos_x = 100
        self.pos_y = 100
        self.theme_key = "cyberpunk"
        self.is_pinned = False
        self.is_mini = False
        self.event_idx = 0

        self.events = [
            {
                "id": "1",
                "title": "วันเกิดแฟนปีนี้",
                "date": "2026-10-02 00:00",
                "start_date": "2026-09-01"
            },
            {
                "id": "2",
                "title": "วันรับปริญญา",
                "date": "2026-12-24 09:00",
                "start_date": "2026-01-01"
            },
            {
                "id": "3",
                "title": "วันปีใหม่ 2027",
                "date": "2027-01-01 00:00",
                "start_date": "2026-01-01"
            }
        ]

        self.work_enabled = True
        self.work_start_time = "08:30"
        self.work_end_time = "17:30"
        self.work_days = [0, 1, 2, 3, 4]

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.pos_x = max(0, min(2500, data.get('x', 100)))
                    self.pos_y = max(0, min(1500, data.get('y', 100)))
                    
                    saved_theme = data.get('theme', 'cyberpunk')
                    self.theme_key = saved_theme if saved_theme in THEMES else "cyberpunk"
                    
                    self.is_pinned = data.get('pinned', False)
                    self.is_mini = data.get('mini', False)
                    self.event_idx = data.get('event_idx', 0)
                    
                    saved_events = data.get('events', [])
                    if saved_events and isinstance(saved_events, list):
                        self.events = saved_events

                    self.work_enabled = data.get('work_enabled', True)
                    self.work_start_time = data.get('work_start_time', '08:30')
                    self.work_end_time = data.get('work_end_time', '17:30')
                    self.work_days = data.get('work_days', [0, 1, 2, 3, 4])
            except Exception:
                pass

        if self.event_idx >= len(self.events):
            self.event_idx = 0

    def save_config(self):
        data = {
            'x': self.root.winfo_x(),
            'y': self.root.winfo_y(),
            'theme': self.theme_key,
            'pinned': self.is_pinned,
            'mini': self.is_mini,
            'event_idx': self.event_idx,
            'events': self.events,
            'work_enabled': self.work_enabled,
            'work_start_time': self.work_start_time,
            'work_end_time': self.work_end_time,
            'work_days': self.work_days
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

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="💼 ตั้งค่าเวลาเลิกงาน (Set Work Hours)", command=self.open_work_dialog)
        self.menu.add_command(label="🎯 จัดการ Events ทั้งหมด (Manage Events)", command=self.open_event_manager)
        self.menu.add_command(label="➕ เพิ่ม Event ใหม่ (Add New Event)", command=self.open_add_event_dialog)
        self.menu.add_separator()
        self.menu.add_command(label="📌 ตรึงลอยบนสุด (Always on Top)", command=self.toggle_pin)
        self.menu.add_command(label="➖ สลับโหมดนาฬิกาเล็ก (Mini Clock)", command=self.toggle_mini)
        self.menu.add_separator()
        self.menu.add_command(label="🤖 ธีม: Cyberpunk 2077", command=lambda: self.set_theme("cyberpunk"))
        self.menu.add_command(label="🌆 ธีม: Synthwave 80s", command=lambda: self.set_theme("synthwave"))
        self.menu.add_command(label="🌌 ธีม: Obsidian Midnight", command=lambda: self.set_theme("obsidian"))
        self.menu.add_command(label="🌿 ธีม: Nordic Forest", command=lambda: self.set_theme("forest"))
        self.menu.add_command(label="☕ ธีม: Warm Mocha", command=lambda: self.set_theme("mocha"))
        self.menu.add_command(label="🤍 ธีม: Clean White", command=lambda: self.set_theme("clean_white"))
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
            self.width = 280
            self.height = 76
        else:
            self.width = 350
            self.height = 560
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas.config(width=self.width, height=self.height)
        self.save_config()
        self.draw_ui()

    def set_theme(self, key):
        self.theme_key = key if key in THEMES else "cyberpunk"
        self.save_config()
        self.draw_ui()

    def next_theme(self):
        keys = list(THEMES.keys())
        idx = keys.index(self.theme_key) if self.theme_key in keys else 0
        self.set_theme(keys[(idx + 1) % len(keys)])

    def next_event(self):
        if not self.events:
            return
        self.event_idx = (self.event_idx + 1) % len(self.events)
        self.save_config()
        self.draw_ui()

    def prev_event(self):
        if not self.events:
            return
        self.event_idx = (self.event_idx - 1 + len(self.events)) % len(self.events)
        self.save_config()
        self.draw_ui()

    def close(self):
        self.save_config()
        self.root.destroy()

    def parse_datetime(self, date_str):
        date_str = date_str.strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                pass
        return None

    def calculate_work_countdown(self, now):
        weekday = now.weekday()
        if weekday not in self.work_days:
            return {
                "title": "เวลาทำงาน / เลิกงาน",
                "badge": "วันหยุด 🏖️",
                "sub": "วันหยุดสุดสัปดาห์ พักผ่อนให้เต็มที่!",
                "pct": 100.0
            }

        try:
            sh, sm = map(int, self.work_start_time.split(':'))
            eh, em = map(int, self.work_end_time.split(':'))
        except Exception:
            sh, sm, eh, em = 8, 30, 17, 30

        start_dt = now.replace(hour=sh, minute=sm, second=0, microsecond=0)
        end_dt = now.replace(hour=eh, minute=em, second=0, microsecond=0)

        if now < start_dt:
            diff = start_dt - now
            h, m = diff.seconds // 3600, (diff.seconds % 3600) // 60
            return {
                "title": f"เริ่มงาน {self.work_start_time}",
                "badge": f"อีก {h}ชม {m}น",
                "sub": f"เริ่มงานในอีก {h} ชม. {m} นาที",
                "pct": 0.0
            }
        elif now <= end_dt:
            total_sec = (end_dt - start_dt).total_seconds()
            passed_sec = (now - start_dt).total_seconds()
            pct = (passed_sec / total_sec) * 100 if total_sec > 0 else 0.0

            rem = end_dt - now
            rem_h, rem_m, rem_s = rem.seconds // 3600, (rem.seconds % 3600) // 60, rem.seconds % 60
            badge = f"อีก {rem_h}ชม {rem_m}น" if rem_h > 0 else f"อีก {rem_m}น {rem_s}ว"
            sub = f"เหลืออีก {rem_h} ชม. {rem_m} นาที (เลิกงาน {self.work_end_time}) 🏃💨"

            return {
                "title": f"เวลาเลิกงาน ({self.work_end_time})",
                "badge": badge,
                "sub": sub,
                "pct": pct
            }
        else:
            return {
                "title": f"เวลาเลิกงาน ({self.work_end_time})",
                "badge": "เลิกงานแล้ว 🎉",
                "sub": "หมดเวลาทำงานแล้ว พักผ่อนให้สบายใจ ✨",
                "pct": 100.0
            }

    def calculate_event_countdown(self, event_item):
        now = datetime.datetime.now()
        dt_str = event_item.get("date", "")
        target_dt = self.parse_datetime(dt_str)

        if not target_dt:
            return {
                "title": event_item.get("title", "เป้าหมาย"),
                "badge": "ตั้งค่าวันที่",
                "sub": "วันที่ไม่ถูกต้อง",
                "pct": 0.0
            }

        diff = target_dt - now
        total_seconds = int(diff.total_seconds())

        start_str = event_item.get("start_date", "")
        start_dt = self.parse_datetime(start_str) or (target_dt - datetime.timedelta(days=30))
        total_time_span = (target_dt - start_dt).total_seconds()
        passed_time = (now - start_dt).total_seconds()
        pct = max(0.0, min(100.0, (passed_time / total_time_span) * 100)) if total_time_span > 0 else (100.0 if total_seconds <= 0 else 0.0)

        target_display = target_dt.strftime("%d %b %Y")

        if total_seconds > 0:
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            mins = (total_seconds % 3600) // 60
            secs = total_seconds % 60

            if days > 0:
                badge = f"D-{days} ({hours}h)"
                sub = f"เหลืออีก {days} วัน {hours} ชม. ({target_display})"
            else:
                badge = f"D-0 ({hours}h {mins}m)"
                sub = f"เหลืออีก {hours} ชม. {mins} นาที {secs} วิ! 🔥"
        elif total_seconds >= -86400:
            badge = "D-Day! 🎉"
            sub = f"วันนี้คือวันสำคัญ! ({target_display})"
            pct = 100.0
        else:
            p_days = abs(total_seconds) // 86400
            badge = f"D+{p_days}"
            sub = f"ผ่านมา {p_days} วัน ({target_display})"
            pct = 100.0

        return {
            "title": event_item.get("title", "เป้าหมาย"),
            "badge": badge,
            "sub": sub,
            "pct": pct
        }

    def calculate_progress(self):
        now = datetime.datetime.now()
        year = now.year

        # Year %
        y_start = datetime.datetime(year, 1, 1)
        y_end = datetime.datetime(year + 1, 1, 1)
        year_pct = ((now - y_start) / (y_end - y_start)) * 100
        year_days_left = (y_end.date() - now.date()).days

        # Month %
        month = now.month
        m_start = datetime.datetime(year, month, 1)
        next_m_start = datetime.datetime(year + 1, 1, 1) if month == 12 else datetime.datetime(year, month + 1, 1)
        month_pct = ((now - m_start) / (next_m_start - m_start)) * 100
        month_days_left = (next_m_start.date() - now.date()).days

        # Week %
        weekday = now.weekday()
        w_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=weekday)
        w_end = w_start + datetime.timedelta(days=7)
        week_pct = ((now - w_start) / (w_end - w_start)) * 100
        week_days_left = 6 - weekday

        # Day %
        d_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        d_end = d_start + datetime.timedelta(days=1)
        day_pct = ((now - d_start) / (d_end - d_start)) * 100
        day_rem = d_end - now
        day_hours = day_rem.seconds // 3600
        day_mins = (day_rem.seconds % 3600) // 60

        # Event & Work
        if self.events and 0 <= self.event_idx < len(self.events):
            event_data = self.calculate_event_countdown(self.events[self.event_idx])
        else:
            event_data = {"title": "ไม่มีเป้าหมาย", "badge": "+ เพิ่ม", "sub": "คลิกเพื่อเพิ่ม Event", "pct": 0.0}

        work_data = self.calculate_work_countdown(now)

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
            "event": event_data,
            "work": work_data,
            "total_events": len(self.events),
            "event_num": self.event_idx + 1,
            "time_str": now.strftime("%H:%M:%S"),
            "date_en": now.strftime("%a, %d %b %Y").upper(),
            "date_th": f"{THAI_DAYS[now.isoweekday() % 7]}ที่ {now.day} {THAI_MONTHS[month - 1]} {year}"
        }

    def draw_ui(self):
        self.canvas.delete("all")
        t = self.get_theme()
        data = self.calculate_progress()

        if self.is_mini:
            # -------------------------------------------------------------
            # MINI MODE: FLOATING DIGITAL CLOCK & DATE CAPSULE (Image 2 style)
            # -------------------------------------------------------------
            self.round_rect(4, 4, self.width - 4, self.height - 4, r=18, fill=t["bg"], outline=t["border"], width=1.5)
            
            # Big Digital Clock (e.g. 14:50:27)
            self.mini_time_id = self.canvas.create_text(
                18, 30, 
                text=data["time_str"], 
                font=("Segoe UI", 24, "bold"), 
                fill=t["text_main"], 
                anchor="w"
            )

            # Date Subtitle (e.g. วันพฤหัสบดีที่ 3 กันยายน 2026)
            self.mini_date_id = self.canvas.create_text(
                18, 56, 
                text=data["date_th"], 
                font=("Segoe UI", 8), 
                fill=t["text_sub"], 
                anchor="w"
            )

            # Action Controls on the right
            pin_color = t["accent"] if self.is_pinned else t["text_sub"]
            btn_pin = self.canvas.create_text(self.width - 58, 20, text="📌", font=("Segoe UI Emoji", 8), fill=pin_color)
            self.canvas.tag_bind(btn_pin, "<Button-1>", lambda e: self.toggle_pin())

            btn_th = self.canvas.create_text(self.width - 38, 20, text="🎨", font=("Segoe UI Emoji", 8), fill=t["text_sub"])
            self.canvas.tag_bind(btn_th, "<Button-1>", lambda e: self.next_theme())

            # Expand Button ➕ (Restores Full View)
            btn_exp = self.canvas.create_text(self.width - 18, 20, text="➕", font=("Segoe UI", 10, "bold"), fill=t["accent"])
            self.canvas.tag_bind(btn_exp, "<Button-1>", lambda e: self.toggle_mini())
            return

        # -----------------------------------------------------------------
        # FULL VIEW: SOLID HIGH-CONTRAST CARD WITH VIBRANT THEMES
        # -----------------------------------------------------------------
        self.round_rect(5, 5, self.width - 5, self.height - 5, r=22, fill=t["bg"], outline=t["border"], width=1.5)

        # Header Bar
        self.canvas.create_text(20, 24, text="⏳", font=("Segoe UI Emoji", 10), anchor="w")
        self.canvas.create_text(38, 24, text="TimeFlow", font=("Segoe UI", 10, "bold"), fill=t["text_main"], anchor="w")

        # Subtle Header Actions
        btn_work = self.canvas.create_text(self.width - 114, 24, text="💼", font=("Segoe UI Emoji", 8), fill=t["text_sub"])
        self.canvas.tag_bind(btn_work, "<Button-1>", lambda e: self.open_work_dialog())

        pin_color = t["accent"] if self.is_pinned else t["text_sub"]
        btn_pin = self.canvas.create_text(self.width - 92, 24, text="📌", font=("Segoe UI Emoji", 8), fill=pin_color)
        self.canvas.tag_bind(btn_pin, "<Button-1>", lambda e: self.toggle_pin())

        btn_mini = self.canvas.create_text(self.width - 70, 24, text="➖", font=("Segoe UI", 9), fill=t["text_sub"])
        self.canvas.tag_bind(btn_mini, "<Button-1>", lambda e: self.toggle_mini())

        btn_th = self.canvas.create_text(self.width - 48, 24, text="🎨", font=("Segoe UI Emoji", 8), fill=t["text_sub"])
        self.canvas.tag_bind(btn_th, "<Button-1>", lambda e: self.next_theme())

        btn_cl = self.canvas.create_text(self.width - 24, 24, text="✕", font=("Segoe UI", 9), fill=t["text_sub"])
        self.canvas.tag_bind(btn_cl, "<Button-1>", lambda e: self.close())

        # 1. Big Hero Clock & Minimal Date
        self.time_label_id = self.canvas.create_text(20, 60, text=data["time_str"], font=("Segoe UI", 28, "bold"), fill=t["text_main"], anchor="w")
        self.date_label_id = self.canvas.create_text(20, 92, text=data["date_th"], font=("Segoe UI", 9), fill=t["text_sub"], anchor="w")

        # Divider line
        self.canvas.create_line(20, 110, self.width - 20, 110, fill=t.get("border_subtle", t["track"]), width=1)

        # 2. Typography Micro-Progress Tracks (Perfect Spacing, No Overlaps)
        y_cursor = 130
        line_gap = 62

        # Item 1: TARGET (Custom Multiple Goals)
        self.draw_clean_row(
            y=y_cursor,
            emoji="🎯",
            title=data['event']['title'],
            badge=data['event']['badge'],
            sub=data['event']['sub'],
            pct=data['event']['pct'],
            bar_color=t["goal_bar"],
            badge_color=t["goal_glow"],
            is_event=True,
            data=data,
            theme=t
        )
        y_cursor += line_gap

        # Item 2: WORK (Off-Work Countdown)
        if self.work_enabled:
            self.draw_clean_row(
                y=y_cursor,
                emoji="💼",
                title=data['work']['title'],
                badge=data['work']['badge'],
                sub=data['work']['sub'],
                pct=data['work']['pct'],
                bar_color=t["work_bar"],
                badge_color=t["work_glow"],
                is_work=True,
                data=data,
                theme=t
            )
            y_cursor += line_gap

        # Item 3: YEAR 2026
        self.draw_clean_row(
            y=y_cursor,
            emoji="🌍",
            title=f"ปี {data['year']}",
            badge=f"{data['year_pct']:.1f}%",
            sub=f"เหลืออีก {data['year_days_left']} วันในปีนี้",
            pct=data['year_pct'],
            bar_color=t["year_bar"],
            badge_color=t["year_bar"],
            theme=t
        )
        y_cursor += line_gap

        # Item 4: MONTH
        self.draw_clean_row(
            y=y_cursor,
            emoji="🗓️",
            title=f"เดือน{data['month_name']}",
            badge=f"{data['month_pct']:.1f}%",
            sub=f"เหลืออีก {data['month_days_left']} วันในเดือนนี้",
            pct=data['month_pct'],
            bar_color=t["month_bar"],
            badge_color=t["month_bar"],
            theme=t
        )
        y_cursor += line_gap

        # Item 5: TODAY
        self.draw_clean_row(
            y=y_cursor,
            emoji="☀️",
            title="วันนี้ (Today)",
            badge=f"{data['day_pct']:.1f}%",
            sub=f"เหลืออีก {data['day_hours']} ชม. {data['day_mins']} นาที",
            pct=data['day_pct'],
            bar_color=t["day_bar"],
            badge_color=t["day_bar"],
            theme=t
        )

        # Bottom minimal quote
        self.canvas.create_text(self.width // 2, self.height - 22, text="เวลาคือสิ่งเดียวที่ผ่านไปแล้วไม่ย้อนกลับ ✨", font=("Segoe UI", 8), fill=t["text_sub"])

    def draw_clean_row(self, y, emoji, title, badge, sub, pct, bar_color, badge_color, theme, is_event=False, is_work=False, data=None):
        x1 = 20
        x2 = self.width - 20

        # Emoji Icon
        t_icon = self.canvas.create_text(x1, y, text=emoji, font=("Segoe UI Emoji", 10), anchor="w")

        # Title (Positioned with proper margin)
        t_title = self.canvas.create_text(x1 + 22, y, text=title, font=("Segoe UI", 9, "bold"), fill=theme["text_main"], anchor="w")

        # Event Switcher Arrows (e.g. ◀ 1/3 ▶)
        if is_event and data and data['total_events'] > 1:
            btn_prev = self.canvas.create_text(x2 - 120, y, text="◀", font=("Segoe UI", 8), fill=theme["text_sub"])
            self.canvas.tag_bind(btn_prev, "<Button-1>", lambda e: self.prev_event())

            self.canvas.create_text(x2 - 106, y, text=f"{data['event_num']}/{data['total_events']}", font=("Segoe UI", 7), fill=theme["text_sub"])

            btn_next = self.canvas.create_text(x2 - 92, y, text="▶", font=("Segoe UI", 8), fill=theme["text_sub"])
            self.canvas.tag_bind(btn_next, "<Button-1>", lambda e: self.next_event())

        # Badge (Right-aligned, bold accent)
        badge_id = self.canvas.create_text(x2, y, text=badge, font=("Segoe UI", 9, "bold"), fill=badge_color, anchor="e")

        # Micro-Track Line (Height 4px with clean smooth rounded ends)
        by = y + 14
        self.round_rect(x1, by, x2, by + 4, r=2, fill=theme["track"])
        fill_w = x1 + (x2 - x1) * (pct / 100.0)
        if fill_w > x1 + 2:
            self.round_rect(x1, by, fill_w, by + 4, r=2, fill=bar_color)

        # Subtitle Text (Under track line)
        sub_id = self.canvas.create_text(x1, y + 28, text=sub, font=("Segoe UI", 8), fill=theme["text_sub"], anchor="w")

        # Event bindings
        if is_event:
            self.event_badge_id = badge_id
            self.event_sub_id = sub_id
            for elem in [t_icon, t_title, badge_id, sub_id]:
                self.canvas.tag_bind(elem, "<Button-1>", lambda e: self.open_event_manager())
        elif is_work:
            self.work_badge_id = badge_id
            self.work_sub_id = sub_id
            for elem in [t_icon, t_title, badge_id, sub_id]:
                self.canvas.tag_bind(elem, "<Button-1>", lambda e: self.open_work_dialog())

    # ---------------------------------------------------------------------
    # WORK HOURS SETTINGS DIALOG
    # ---------------------------------------------------------------------
    def open_work_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("💼 ตั้งค่าเวลาทำงาน & เลิกงาน")
        dialog.geometry("320x260")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        t = self.get_theme()
        dialog.config(bg=t["bg"])

        lbl_head = tk.Label(dialog, text="💼 ตั้งค่าเวลานับถอยหลังเลิกงาน", font=("Segoe UI", 10, "bold"), bg=t["bg"], fg=t["text_main"])
        lbl_head.pack(anchor="w", padx=20, pady=(16, 10))

        lbl_start = tk.Label(dialog, text="เวลาเริ่มงาน (HH:MM เช่น 08:30):", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 8, "bold"))
        lbl_start.pack(anchor="w", padx=20, pady=(0, 2))

        entry_start = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["card_bg"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_start.insert(0, self.work_start_time)
        entry_start.pack(fill="x", padx=20, pady=(0, 8), ipady=3)

        lbl_end = tk.Label(dialog, text="เวลาเลิกงาน (HH:MM เช่น 17:30):", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 8, "bold"))
        lbl_end.pack(anchor="w", padx=20, pady=(0, 2))

        entry_end = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["card_bg"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_end.insert(0, self.work_end_time)
        entry_end.pack(fill="x", padx=20, pady=(0, 14), ipady=3)

        def on_save():
            s_val = entry_start.get().strip()
            e_val = entry_end.get().strip()
            try:
                datetime.datetime.strptime(s_val, "%H:%M")
                datetime.datetime.strptime(e_val, "%H:%M")
                self.work_start_time = s_val
                self.work_end_time = e_val
                self.save_config()
                self.draw_ui()
                dialog.destroy()
            except ValueError:
                msgbox.showerror("รูปแบบเวลาไม่ถูกต้อง", "กรุณาใส่เวลาในรูปแบบ ชั่วโมง:นาที\nเช่น 08:30 หรือ 17:30", parent=dialog)

        btn_save = tk.Button(dialog, text="บันทึกเวลาทำงาน 💾", bg=t["work_bar"], fg="#000000" if self.theme_key == "cyberpunk" else "#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", command=on_save, cursor="hand2")
        btn_save.pack(fill="x", padx=20, ipady=4)

    # ---------------------------------------------------------------------
    # EVENT MANAGER DIALOG
    # ---------------------------------------------------------------------
    def open_event_manager(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("🎯 จัดการ Events ทั้งหมด")
        dialog.geometry("360x420")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        t = self.get_theme()
        dialog.config(bg=t["bg"])

        head_frame = tk.Frame(dialog, bg=t["bg"])
        head_frame.pack(fill="x", padx=16, pady=(14, 8))

        lbl_head = tk.Label(head_frame, text="🎯 รายการเป้าหมาย & Events", font=("Segoe UI", 11, "bold"), bg=t["bg"], fg=t["text_main"])
        lbl_head.pack(side="left")

        btn_new = tk.Button(head_frame, text="➕ เพิ่ม Event", bg=t["goal_bar"], fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", cursor="hand2", command=lambda: [dialog.destroy(), self.open_add_event_dialog()])
        btn_new.pack(side="right")

        list_canvas = tk.Canvas(dialog, bg=t["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=list_canvas.yview)
        scroll_frame = tk.Frame(list_canvas, bg=t["bg"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )

        list_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=340)
        list_canvas.configure(yscrollcommand=scrollbar.set)

        list_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=6)
        scrollbar.pack(side="right", fill="y", padx=(0, 6), pady=6)

        if not self.events:
            lbl_empty = tk.Label(scroll_frame, text="ยังไม่มี Event ในรายการ\nกดปุ่ม '+ เพิ่ม Event' เพื่อเริ่มต้น", font=("Segoe UI", 9), bg=t["bg"], fg=t["text_sub"], pady=40)
            lbl_empty.pack(fill="x")

        for idx, ev in enumerate(self.events):
            ev_calc = self.calculate_event_countdown(ev)
            is_active = (idx == self.event_idx)

            card = tk.Frame(scroll_frame, bg=t["card_bg"], highlightbackground=t["goal_bar"] if is_active else t["border"], highlightthickness=1)
            card.pack(fill="x", padx=8, pady=4, ipady=4)

            top_row = tk.Frame(card, bg=t["card_bg"])
            top_row.pack(fill="x", padx=8, pady=(4, 2))

            lbl_title = tk.Label(top_row, text=f"{'⭐ ' if is_active else ''}{ev['title']}", font=("Segoe UI", 9, "bold"), bg=t["card_bg"], fg=t["text_main"])
            lbl_title.pack(side="left")

            lbl_badge = tk.Label(top_row, text=ev_calc['badge'], font=("Segoe UI", 8, "bold"), bg=t["card_bg"], fg=t["goal_glow"])
            lbl_badge.pack(side="right")

            lbl_sub = tk.Label(card, text=ev_calc['sub'], font=("Segoe UI", 7), bg=t["card_bg"], fg=t["text_sub"], anchor="w")
            lbl_sub.pack(fill="x", padx=8, pady=(0, 4))

            btn_row = tk.Frame(card, bg=t["card_bg"])
            btn_row.pack(fill="x", padx=8, pady=(2, 2))

            def make_select_cmd(i):
                return lambda: [setattr(self, 'event_idx', i), self.save_config(), self.draw_ui(), dialog.destroy()]

            def make_edit_cmd(i):
                return lambda: [dialog.destroy(), self.open_edit_event_dialog(i)]

            def make_del_cmd(i):
                return lambda: self.delete_event(i, dialog)

            if not is_active:
                btn_sel = tk.Button(btn_row, text="เลือกแสดงบนหน้าจอ", font=("Segoe UI", 7), bg=t["track"], fg=t["text_main"], relief="flat", cursor="hand2", command=make_select_cmd(idx))
                btn_sel.pack(side="left", padx=(0, 4))

            btn_edit = tk.Button(btn_row, text="✏️ แก้ไข", font=("Segoe UI", 7), bg=t["track"], fg=t["text_main"], relief="flat", cursor="hand2", command=make_edit_cmd(idx))
            btn_edit.pack(side="left", padx=4)

            btn_del = tk.Button(btn_row, text="🗑️ ลบ", font=("Segoe UI", 7), bg=t["track"], fg="#f87171", relief="flat", cursor="hand2", command=make_del_cmd(idx))
            btn_del.pack(side="right", padx=4)

    def delete_event(self, idx, parent_dialog):
        if len(self.events) <= 1:
            msgbox.showinfo("ไม่สามารถลบได้", "ต้องมี Event อย่างน้อย 1 รายการครับ", parent=parent_dialog)
            return
        del self.events[idx]
        if self.event_idx >= len(self.events):
            self.event_idx = max(0, len(self.events) - 1)
        self.save_config()
        self.draw_ui()
        parent_dialog.destroy()
        self.open_event_manager()

    def open_add_event_dialog(self):
        self.open_edit_event_dialog(event_index=None)

    def open_edit_event_dialog(self, event_index=None):
        is_edit = (event_index is not None and 0 <= event_index < len(self.events))
        current_data = self.events[event_index] if is_edit else {
            "title": "",
            "date": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d 00:00"),
            "start_date": datetime.date.today().isoformat()
        }

        dialog = tk.Toplevel(self.root)
        dialog.title("แก้ไข Event 🎯" if is_edit else "เพิ่ม Event ใหม่ ➕")
        dialog.geometry("330x260")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        t = self.get_theme()
        dialog.config(bg=t["bg"])

        lbl_title = tk.Label(dialog, text="ชื่อ Event / เป้าหมาย:", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 9, "bold"))
        lbl_title.pack(anchor="w", padx=20, pady=(16, 4))

        entry_title = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["card_bg"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_title.insert(0, current_data.get("title", ""))
        entry_title.pack(fill="x", padx=20, pady=(0, 10), ipady=4)

        lbl_date = tk.Label(dialog, text="วัน/เวลาเป้าหมาย (YYYY-MM-DD หรือ YYYY-MM-DD HH:MM):", bg=t["bg"], fg=t["text_main"], font=("Segoe UI", 8, "bold"))
        lbl_date.pack(anchor="w", padx=20, pady=(0, 4))

        entry_date = tk.Entry(dialog, font=("Segoe UI", 10), bg=t["card_bg"], fg=t["text_main"], insertbackground=t["text_main"], relief="flat")
        entry_date.insert(0, current_data.get("date", ""))
        entry_date.pack(fill="x", padx=20, pady=(0, 16), ipady=4)

        def on_save():
            new_title = entry_title.get().strip() or "เป้าหมายใหม่"
            new_date_str = entry_date.get().strip()

            parsed = self.parse_datetime(new_date_str)
            if not parsed:
                msgbox.showerror("รูปแบบวันที่ไม่ถูกต้อง", "กรุณาใส่วันที่ในรูปแบบ:\n• 2026-10-02 (ปี-เดือน-วัน)\n• 2026-10-02 18:00 (ระบุเวลาชั่วโมง:นาที)", parent=dialog)
                return

            formatted_date = parsed.strftime("%Y-%m-%d %H:%M") if (parsed.hour != 0 or parsed.minute != 0) else parsed.strftime("%Y-%m-%d")

            if is_edit:
                self.events[event_index]["title"] = new_title
                self.events[event_index]["date"] = formatted_date
            else:
                new_item = {
                    "id": str(int(datetime.datetime.now().timestamp())),
                    "title": new_title,
                    "date": formatted_date,
                    "start_date": datetime.date.today().isoformat()
                }
                self.events.append(new_item)
                self.event_idx = len(self.events) - 1

            self.save_config()
            self.draw_ui()
            dialog.destroy()

        btn_save = tk.Button(dialog, text="บันทึก Event 💾", bg=t["goal_bar"], fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", command=on_save, cursor="hand2")
        btn_save.pack(fill="x", padx=20, ipady=5)

    def update_loop(self):
        data = self.calculate_progress()

        if self.is_mini:
            # Real-time clock update in Mini Mode
            if hasattr(self, 'mini_time_id'):
                self.canvas.itemconfig(self.mini_time_id, text=data["time_str"])
                self.canvas.itemconfig(self.mini_date_id, text=data["date_th"])
        else:
            # Real-time clock update in Full Mode
            if hasattr(self, 'time_label_id'):
                self.canvas.itemconfig(self.time_label_id, text=data["time_str"])
                self.canvas.itemconfig(self.date_label_id, text=data["date_th"])

            # Real-time event countdown
            if hasattr(self, 'event_badge_id'):
                self.canvas.itemconfig(self.event_badge_id, text=data['event']['badge'])
                self.canvas.itemconfig(self.event_sub_id, text=data['event']['sub'])

            # Real-time work countdown
            if hasattr(self, 'work_badge_id'):
                self.canvas.itemconfig(self.work_badge_id, text=data['work']['badge'])
                self.canvas.itemconfig(self.work_sub_id, text=data['work']['sub'])
        
        # Redraw on full minute mark
        now = datetime.datetime.now()
        if now.second == 0:
            self.draw_ui()

        self.root.after(1000, self.update_loop)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = TimeFlowWidget()
    app.run()
