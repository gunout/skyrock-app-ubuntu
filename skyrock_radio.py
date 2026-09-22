import sys
import math
import os
import random
import webbrowser
import mpv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QListWidget,
                              QListWidgetItem, QLabel, QFrame, QSlider,
                              QDialog, QGridLayout)
from PyQt6.QtCore import (Qt, QTimer, QSize, QPropertyAnimation,
                          QEasingCurve, QRectF, QPoint)
from PyQt6.QtGui import (QFont, QColor, QIcon, QPixmap, QPainter, QPainterPath,
                         QPen, QCursor, QLinearGradient, QBrush)


# ============================================================
#  FLUX RADIO — Skyrock (Toutes les webradios)
# ============================================================
STATIONS = [
    ("SKYROCK", "https://icecast.skyrock.net/s/natio_aac_128k"),
    ("RAP & RNB NON-STOP", "https://icecast.skyrock.net/s/rap_rnb_aac_128k"),
    ("100% FRANÇAIS", "https://icecast.skyrock.net/s/francais_aac_128k"),
    ("KLASSIKS", "https://icecast.skyrock.net/s/klassiks_aac_128k"),
    ("URBAN MUSIC", "https://icecast.skyrock.net/s/urban_music_aac_128k"),
    ("HIT US", "https://icecast.skyrock.net/s/hit_us_aac_128k"),
    ("PLM", "https://icecast.skyrock.net/s/plm_aac_128k"),
    ("ABIDJAN", "https://icecast.skyrock.net/s/abidjan_aac_64k"),
]

# ============================================================
#  LIENS DU SITE OFFICIEL — Skyrock
# ============================================================
SITE_LINKS = {
    "site":      ("Skyrock.fm",         "https://skyrock.fm/"),
    "replay":    ("Replay & Podcasts",  "https://skyrock.fm/replay"),
    "planete":   ("Planète Rap",        "https://skyrock.fm/planete-rap"),
    "radios":    ("Webradios",          "https://skyrock.fm/radios"),
    "app":       ("Application Skyrock", "https://skyrock.fm/app/"),
}

# ============================================================
#  CHEMIN DU LOGO
# ============================================================
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")


# ----- Palette -----
BG          = "rgba(12, 12, 14, 240)"
POPUP_BG    = "rgba(18, 18, 22, 250)"
SURFACE     = "rgba(255, 255, 255, 6)"
SURFACE_HOV = "rgba(255, 255, 255, 14)"
ACCENT      = "#ff3b3b"
ACCENT_SOFT = "rgba(255, 59, 59, 22)"
TEXT        = "#f5f5f7"
TEXT_DIM    = "rgba(245, 245, 247, 100)"
SIGNATURE   = "rgba(245, 245, 247, 30)"
CHEVRON     = "rgba(245, 245, 247, 150)"


STYLE = f"""
QMainWindow, QWidget#root {{
    background: {BG};
    border-radius: 14px;
    border: none;
}}

QLabel#logo {{
    background: transparent;
    padding: 2px 4px;
}}

QLabel#signature {{
    color: {SIGNATURE};
    font-size: 9px;
    letter-spacing: 3px;
    padding: 0 8px 4px 8px;
}}

QListWidget#stations {{
    background: rgba(255, 255, 255, 4);
    color: {TEXT};
    border: none;
    border-radius: 10px;
    padding: 6px;
    font-size: 12px;
    letter-spacing: 2px;
    outline: none;
}}
QListWidget#stations::item {{
    padding: 10px 14px;
    border-radius: 8px;
    margin: 2px 0;
}}
QListWidget#stations::item:hover {{
    background: {SURFACE_HOV};
}}
QListWidget#stations::item:selected {{
    background: {ACCENT_SOFT};
    color: {ACCENT};
}}

QFrame#stage {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0a0d12,
                stop:0.5 #06080b,
                stop:1 #04060a);
    border: none;
    border-radius: 12px;
}}

QFrame#controls {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(0,0,0,0),
                stop:0.4 rgba(0,0,0,120),
                stop:1 rgba(0,0,0,180));
    border: none;
    border-bottom-left-radius: 12px;
    border-bottom-right-radius: 12px;
}}

QPushButton#ctrl {{
    background: transparent;
    border: none;
    border-radius: 15px;
    padding: 4px;
    min-width: 30px;
    min-height: 30px;
}}
QPushButton#ctrl:hover {{
    background: {SURFACE_HOV};
}}

QPushButton#site {{
    background: {SURFACE};
    color: {TEXT};
    border: none;
    border-radius: 15px;
    padding: 5px 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
}}
QPushButton#site:hover {{
    background: {ACCENT_SOFT};
    color: {ACCENT};
}}

QDialog#popup {{
    background: {POPUP_BG};
    border: 1px solid rgba(255, 255, 255, 12);
    border-radius: 14px;
}}

QLabel#popup_title {{
    color: {TEXT};
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 4px;
    padding: 4px;
}}

QLabel#popup_sub {{
    color: {TEXT_DIM};
    font-size: 10px;
    letter-spacing: 2px;
    padding: 0 4px 6px 4px;
}}

QPushButton#popup_item {{
    background: {SURFACE};
    color: {TEXT};
    border: none;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 11px;
    letter-spacing: 1px;
    text-align: left;
}}
QPushButton#popup_item:hover {{
    background: {ACCENT_SOFT};
    color: {ACCENT};
}}
QPushButton#popup_item:pressed {{
    background: rgba(255, 59, 59, 40);
}}

QPushButton#popup_close {{
    background: transparent;
    color: {TEXT_DIM};
    border: none;
    border-radius: 15px;
    padding: 4px;
    min-width: 30px;
    min-height: 30px;
}}
QPushButton#popup_close:hover {{
    background: {SURFACE_HOV};
    color: {TEXT};
}}

QSlider::groove:horizontal {{
    height: 3px;
    background: rgba(255,255,255,12);
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: #fff;
    width: 10px;
    height: 10px;
    margin: -4px 0;
    border-radius: 5px;
    border: none;
}}
QSlider::handle:horizontal:hover {{
    background: {ACCENT};
    width: 12px;
    height: 12px;
    margin: -5px 0;
    border-radius: 6px;
}}

QLabel#status {{
    color: {TEXT_DIM};
    font-size: 10px;
    letter-spacing: 2px;
    padding: 2px 6px;
}}

QLabel#time {{
    color: {TEXT_DIM};
    font-size: 10px;
    letter-spacing: 0.5px;
    min-width: 80px;
}}

QLabel#nowplaying {{
    color: {TEXT};
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 3px;
}}

QLabel#nowmeta {{
    color: {TEXT_DIM};
    font-size: 10px;
    letter-spacing: 2px;
}}
"""


# ================= ICÔNES =================
def _make_icon(kind, size=16, color="#f5f5f7"):
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(1.4)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(QColor(color))
    s = size

    if kind == "play":
        path = QPainterPath()
        path.moveTo(s*0.32, s*0.24)
        path.lineTo(s*0.76, s*0.50)
        path.lineTo(s*0.32, s*0.76)
        path.closeSubpath()
        p.drawPath(path)
    elif kind == "pause":
        p.drawRoundedRect(int(s*0.32), int(s*0.24), int(s*0.12), int(s*0.52), 2, 2)
        p.drawRoundedRect(int(s*0.56), int(s*0.24), int(s*0.12), int(s*0.52), 2, 2)
    elif kind == "stop":
        p.drawRoundedRect(int(s*0.32), int(s*0.32), int(s*0.36), int(s*0.36), 3, 3)
    elif kind == "volume":
        path = QPainterPath()
        path.moveTo(s*0.20, s*0.42)
        path.lineTo(s*0.34, s*0.42)
        path.lineTo(s*0.48, s*0.28)
        path.lineTo(s*0.48, s*0.72)
        path.lineTo(s*0.34, s*0.58)
        path.lineTo(s*0.20, s*0.58)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawArc(int(s*0.44), int(s*0.34), int(s*0.24), int(s*0.32), -50*16, 100*16)
    elif kind == "mute":
        path = QPainterPath()
        path.moveTo(s*0.20, s*0.42)
        path.lineTo(s*0.34, s*0.42)
        path.lineTo(s*0.48, s*0.28)
        path.lineTo(s*0.48, s*0.72)
        path.lineTo(s*0.34, s*0.58)
        path.lineTo(s*0.20, s*0.58)
        path.closeSubpath()
        p.drawPath(path)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.60), int(s*0.38), int(s*0.80), int(s*0.62))
        p.drawLine(int(s*0.80), int(s*0.38), int(s*0.60), int(s*0.62))
    elif kind == "close":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.30), int(s*0.70), int(s*0.70))
        p.drawLine(int(s*0.70), int(s*0.30), int(s*0.30), int(s*0.70))
    elif kind == "min":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.28), int(s*0.52), int(s*0.72), int(s*0.52))
    elif kind == "chevron-down":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.42), int(s*0.50), int(s*0.62))
        p.drawLine(int(s*0.50), int(s*0.62), int(s*0.70), int(s*0.42))
    elif kind == "chevron-up":
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawLine(int(s*0.30), int(s*0.58), int(s*0.50), int(s*0.38))
        p.drawLine(int(s*0.50), int(s*0.38), int(s*0.70), int(s*0.58))

    p.end()
    return QIcon(pm)


# ================= VISUALISEUR =================
class Visualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.bars = 32
        self.values = [0.0] * self.bars
        self.targets = [0.0] * self.bars
        self.phase = 0.0
        self.playing = False

        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

    def set_playing(self, playing):
        self.playing = playing

    def _tick(self):
        self.phase += 0.15
        for i in range(self.bars):
            if self.playing:
                base = 0.35 + 0.35 * abs(math.sin(self.phase + i * 0.35))
                self.targets[i] = base + random.uniform(-0.15, 0.25)
            else:
                self.targets[i] = 0.02
            self.targets[i] = max(0.02, min(1.0, self.targets[i]))
            self.values[i] += (self.targets[i] - self.values[i]) * 0.25
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return

        bar_w = w / self.bars * 0.55
        gap = w / self.bars
        cy = h / 2
        max_h = h * 0.55

        grad = QLinearGradient(0, cy - max_h/2, 0, cy + max_h/2)
        grad.setColorAt(0.0, QColor(255, 59, 59, 220))
        grad.setColorAt(0.5, QColor(255, 59, 59, 140))
        grad.setColorAt(1.0, QColor(255, 59, 59, 40))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.PenStyle.NoPen)

        for i, v in enumerate(self.values):
            bh = max(2, v * max_h)
            x = i * gap + (gap - bar_w) / 2
            y = cy - bh / 2
            p.drawRoundedRect(QRectF(x, y, bar_w, bh), bar_w/2, bar_w/2)
        p.end()


# ================= POPUP MENU SITE =================
class SitePopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("popup")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setModal(True)
        self.setFixedSize(380, 380)

        if parent:
            geo = parent.geometry()
            self.move(geo.center() - self.rect().center())

        self.setStyleSheet(STYLE)

        root = QWidget(self)
        root.setObjectName("popup")
        root.setGeometry(self.rect())

        layout = QVBoxLayout(root)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(6)

        title = QLabel("SKYROCK.FM")
        title.setObjectName("popup_title")
        header.addWidget(title)

        header.addStretch()

        btn_close = QPushButton()
        btn_close.setObjectName("popup_close")
        btn_close.setIcon(_make_icon("close", 14, TEXT))
        btn_close.setIconSize(QSize(14, 14))
        btn_close.clicked.connect(self.reject)
        header.addWidget(btn_close)

        layout.addLayout(header)

        sub = QLabel("Ouvrir une section du site officiel")
        sub.setObjectName("popup_sub")
        layout.addWidget(sub)

        grid = QGridLayout()
        grid.setSpacing(6)

        items = [
            ("site",    "Site"),
            ("replay",  "Replay"),
            ("planete", "Planète Rap"),
            ("radios",  "Webradios"),
            ("app",     "Application"),
        ]

        for i, (key, label) in enumerate(items):
            btn = QPushButton(label)
            btn.setObjectName("popup_item")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(lambda _, k=key: self._open(k))
            grid.addWidget(btn, i // 3, i % 3)

        layout.addLayout(grid)
        layout.addStretch()

        foot = QHBoxLayout()
        foot.setSpacing(6)

        btn_all = QPushButton("TOUT OUVRIR")
        btn_all.setObjectName("popup_item")
        btn_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_all.clicked.connect(self._open_all)
        foot.addWidget(btn_all, stretch=1)

        btn_quit = QPushButton("FERMER")
        btn_quit.setObjectName("popup_item")
        btn_quit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_quit.clicked.connect(self.reject)
        foot.addWidget(btn_quit)

        layout.addLayout(foot)

    def _open(self, key):
        if key in SITE_LINKS:
            _, url = SITE_LINKS[key]
            webbrowser.open(url)
        self.accept()

    def _open_all(self):
        for key in ("site", "replay", "planete", "radios", "app"):
            if key in SITE_LINKS:
                _, url = SITE_LINKS[key]
                webbrowser.open(url)
        self.accept()


# ================= FENÊTRE =================
class Skyrock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RADIO SKYROCK")
        self.resize(450, 420)
        self.setMinimumSize(320, 280)
        self.player = None
        self._drag_pos = None
        self._resize_edge = None
        self._resize_margin = 6
        self._controls_collapsed = False
        self._controls_full_height = 0
        self._window_folded = False
        self._unfolded_height = 420
        self._current_station = "AUCUNE STATION"
        self.setMouseTracking(True)
        self.setStyleSheet(STYLE)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # --- HUD top ---
        top = QHBoxLayout()
        top.setSpacing(8)

        self.logo = QLabel()
        self.logo.setObjectName("logo")
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            pix = pix.scaledToHeight(28, Qt.TransformationMode.SmoothTransformation)
            self.logo.setPixmap(pix)
        else:
            self.logo.setText("SKYROCK")
            self.logo.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 700; letter-spacing: 4px;")
        self.logo.setFixedHeight(30)
        top.addWidget(self.logo)

        btn_site = QPushButton("SITES")
        btn_site.setObjectName("site")
        btn_site.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_site.clicked.connect(self.open_site_popup)
        top.addWidget(btn_site)

        top.addStretch()

        btn_min = QPushButton()
        btn_min.setObjectName("ctrl")
        btn_min.setIcon(_make_icon("min", 14, TEXT))
        btn_min.setIconSize(QSize(14, 14))
        btn_min.clicked.connect(self.showMinimized)
        top.addWidget(btn_min)

        btn_close = QPushButton()
        btn_close.setObjectName("ctrl")
        btn_close.setIcon(_make_icon("close", 14, TEXT))
        btn_close.setIconSize(QSize(14, 14))
        btn_close.clicked.connect(self.close)
        top.addWidget(btn_close)

        self.btn_fold = QPushButton()
        self.btn_fold.setObjectName("ctrl")
        self.btn_fold.setIcon(_make_icon("chevron-up", 14, CHEVRON))
        self.btn_fold.setIconSize(QSize(14, 14))
        self.btn_fold.setToolTip("Replier la fenêtre")
        self.btn_fold.clicked.connect(self.toggle_window_fold)
        top.addWidget(self.btn_fold)

        layout.addLayout(top)

        self.signature = QLabel("by gleaphe")
        self.signature.setObjectName("signature")
        layout.addWidget(self.signature)

        # --- Stage ---
        self.stage = QFrame()
        self.stage.setObjectName("stage")
        v_layout = QVBoxLayout(self.stage)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(0)

        self.stage_body = QWidget()
        body_layout = QVBoxLayout(self.stage_body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.viz = Visualizer(self.stage_body)
        body_layout.addWidget(self.viz, stretch=1)

        v_layout.addWidget(self.stage_body, stretch=1)

        self.overlay = QWidget(self.stage_body)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        ov = QVBoxLayout(self.overlay)
        ov.setContentsMargins(0, 0, 0, 0)
        ov.addStretch()

        self.lbl_now = QLabel(self._current_station)
        self.lbl_now.setObjectName("nowplaying")
        self.lbl_now.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ov.addWidget(self.lbl_now)

        ov.addSpacing(4)

        self.lbl_meta = QLabel("EN ATTENTE")
        self.lbl_meta.setObjectName("nowmeta")
        self.lbl_meta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ov.addWidget(self.lbl_meta)

        ov.addStretch()

        # --- Contrôles ---
        self.controls = QFrame()
        self.controls.setObjectName("controls")
        c_layout = QVBoxLayout(self.controls)
        c_layout.setContentsMargins(12, 6, 12, 8)
        c_layout.setSpacing(4)

        row = QHBoxLayout()
        row.setSpacing(4)

        self.btn_play = QPushButton()
        self.btn_play.setObjectName("ctrl")
        self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        self.btn_play.setIconSize(QSize(16, 16))
        self.btn_play.clicked.connect(self.toggle_pause)
        row.addWidget(self.btn_play)

        self.btn_stop = QPushButton()
        self.btn_stop.setObjectName("ctrl")
        self.btn_stop.setIcon(_make_icon("stop", 12, TEXT))
        self.btn_stop.setIconSize(QSize(12, 12))
        self.btn_stop.clicked.connect(self.stop)
        row.addWidget(self.btn_stop)

        self.time_lbl = QLabel("EN DIRECT")
        self.time_lbl.setObjectName("time")
        row.addWidget(self.time_lbl)

        row.addStretch()

        self.btn_mute = QPushButton()
        self.btn_mute.setObjectName("ctrl")
        self.btn_mute.setIcon(_make_icon("volume", 14, TEXT))
        self.btn_mute.setIconSize(QSize(14, 14))
        self.btn_mute.clicked.connect(self.toggle_mute)
        row.addWidget(self.btn_mute)

        self.vol = QSlider(Qt.Orientation.Horizontal)
        self.vol.setRange(0, 100)
        self.vol.setValue(80)
        self.vol.setFixedWidth(80)
        self.vol.valueChanged.connect(self.set_volume)
        row.addWidget(self.vol)

        self.btn_toggle = QPushButton()
        self.btn_toggle.setObjectName("ctrl")
        self.btn_toggle.setIcon(_make_icon("chevron-down", 12, CHEVRON))
        self.btn_toggle.setIconSize(QSize(12, 12))
        self.btn_toggle.clicked.connect(self.toggle_controls)
        row.addWidget(self.btn_toggle)

        c_layout.addLayout(row)
        v_layout.addWidget(self.controls)

        # Bouton flottant
        self.btn_reopen = QPushButton(self.stage)
        self.btn_reopen.setObjectName("ctrl")
        self.btn_reopen.setIcon(_make_icon("chevron-up", 14, CHEVRON))
        self.btn_reopen.setIconSize(QSize(14, 14))
        self.btn_reopen.setFixedSize(30, 30)
        self.btn_reopen.setStyleSheet("""
            QPushButton {
                background: rgba(12, 12, 14, 180);
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background: rgba(255, 59, 59, 40);
            }
        """)
        self.btn_reopen.clicked.connect(self.toggle_controls)
        self.btn_reopen.hide()

        layout.addWidget(self.stage, stretch=1)

        # --- Liste stations ---
        header = QLabel("STATIONS SKYROCK")
        header.setObjectName("status")
        layout.addWidget(header)

        self.stations = QListWidget()
        self.stations.setObjectName("stations")
        self.stations.setMaximumHeight(160)
        self.stations.itemDoubleClicked.connect(self._play_station_item)
        self.stations.itemActivated.connect(self._play_station_item)

        for name, url in STATIONS:
            it = QListWidgetItem(name)
            it.setData(Qt.ItemDataRole.UserRole, url)
            self.stations.addItem(it)

        layout.addWidget(self.stations)

        self.status = QLabel("PRÊT")
        self.status.setObjectName("status")
        layout.addWidget(self.status)

        # Timers
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.setInterval(3500)
        self.hide_timer.timeout.connect(self._auto_hide_controls)

    # ===== Popup site =====
    def open_site_popup(self):
        popup = SitePopup(self)
        popup.exec()

    # ===== mpv =====
    def showEvent(self, event):
        super().showEvent(event)
        if self.player is None:
            self.player = mpv.MPV(
                vo='null',
                ao='pulse',
                ytdl=False,
                cache=True,
                cache_secs=2,
                demuxer_max_bytes='2M',
                demuxer_max_back_bytes='1M',
                demuxer_readahead_secs=1,
                network_timeout=15,
                audio_client_name='Skyrock',
                force_window='no',
                idle='yes',
            )
            self.player.volume = self.vol.value()

    # ===== Lecture =====
    def _play_station_item(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        name = item.text()
        self._play(url, name)

    def _play(self, url, name):
        if self.player is None:
            self.status.setText("LECTEUR NON PRÊT")
            return

        try:
            self.player.command('stop')
            self.player.pause = False
            self.player.mute = False
        except Exception:
            pass

        self._current_station = name.upper()
        self.lbl_now.setText(self._current_station)
        self.lbl_meta.setText("CONNEXION...")
        self.btn_play.setIcon(_make_icon("pause", 16, TEXT))
        self.viz.set_playing(True)
        self.status.setText(f"LECTURE : {name.upper()}")
        self._reset_auto_hide()

        def _do_play():
            try:
                self.player.play(url)
                self.lbl_meta.setText("EN DIRECT")
            except Exception as ex:
                self.status.setText(f"ERREUR : {ex}")

        QTimer.singleShot(200, _do_play)

    def toggle_pause(self):
        if not self.player:
            return
        self.player.pause = not self.player.pause
        paused = self.player.pause
        self.btn_play.setIcon(_make_icon("play" if paused else "pause", 16, TEXT))
        self.viz.set_playing(not paused)
        self.lbl_meta.setText("PAUSE" if paused else "EN DIRECT")

    def stop(self):
        if self.player:
            self.player.command('stop')
        self.btn_play.setIcon(_make_icon("play", 16, TEXT))
        self.viz.set_playing(False)
        self.lbl_now.setText("AUCUNE STATION")
        self.lbl_meta.setText("EN ATTENTE")
        self.status.setText("ARRÊTÉ")

    def toggle_mute(self):
        if not self.player:
            return
        self.player.mute = not self.player.mute
        self.btn_mute.setIcon(_make_icon("mute" if self.player.mute else "volume", 14, TEXT))

    def set_volume(self, v):
        if self.player:
            self.player.volume = v

    # ===== Replis fenêtre =====
    def toggle_window_fold(self):
        if self._window_folded:
            self.stage.show()
            self.signature.show()
            self.status.show()
            self.stations.show()
            target_h = self._unfolded_height
            self.btn_fold.setIcon(_make_icon("chevron-up", 14, CHEVRON))
            self._window_folded = False
            self.setMinimumSize(320, 280)
        else:
            self._unfolded_height = self.height()
            self.stage.hide()
            self.signature.hide()
            self.status.hide()
            self.stations.hide()
            target_h = 70
            self.btn_fold.setIcon(_make_icon("chevron-down", 14, CHEVRON))
            self._window_folded = True
            self.setMinimumSize(280, target_h)

        self.anim_fold = QPropertyAnimation(self, b"size")
        self.anim_fold.setDuration(240)
        self.anim_fold.setStartValue(self.size())
        self.anim_fold.setEndValue(QSize(self.width(), target_h))
        self.anim_fold.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim_fold.start()

    # ===== Auto-hide contrôles =====
    def _reset_auto_hide(self):
        if self._controls_collapsed or self._window_folded:
            return
        self.hide_timer.start()

    def _auto_hide_controls(self):
        if self._controls_collapsed or self._window_folded:
            return
        if self.controls.underMouse() or self.btn_reopen.underMouse():
            self.hide_timer.start()
            return
        self._controls_collapsed = True
        self._controls_full_height = self.controls.height()
        self.btn_toggle.setIcon(_make_icon("chevron-up", 12, CHEVRON))
        self.btn_reopen.show()
        self.btn_reopen.raise_()
        self._place_reopen_button()

        self.anim = QPropertyAnimation(self.controls, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.controls.height())
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.start()

    def toggle_controls(self):
        if self._controls_collapsed:
            target = self._controls_full_height or 60
            self.btn_toggle.setIcon(_make_icon("chevron-down", 12, CHEVRON))
            self._controls_collapsed = False
            self.btn_reopen.hide()
        else:
            self._controls_full_height = self.controls.height()
            target = 0
            self.btn_toggle.setIcon(_make_icon("chevron-up", 12, CHEVRON))
            self._controls_collapsed = True
            self.btn_reopen.show()
            self.btn_reopen.raise_()
            self._place_reopen_button()

        self.anim = QPropertyAnimation(self.controls, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setStartValue(self.controls.height())
        self.anim.setEndValue(target)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.anim.start()

        if not self._controls_collapsed:
            self._reset_auto_hide()

    def _place_reopen_button(self):
        w = self.stage.width()
        h = self.stage.height()
        self.btn_reopen.move(w - 44, h - 44)

    # ===== Resize & drag =====
    def _edge_at(self, pos):
        if self._window_folded:
            return None
        m = self._resize_margin
        r = self.rect()
        x, y = pos.x(), pos.y()
        left, right = x <= m, x >= r.width() - m
        top, bottom = y <= m, y >= r.height() - m
        if top and left:     return "NW"
        if top and right:    return "NE"
        if bottom and left:  return "SW"
        if bottom and right: return "SE"
        if left:             return "W"
        if right:            return "E"
        if top:              return "N"
        if bottom:           return "S"
        return None

    def _cursor_for_edge(self, edge):
        return {
            "N": Qt.CursorShape.SizeVerCursor, "S": Qt.CursorShape.SizeVerCursor,
            "E": Qt.CursorShape.SizeHorCursor, "W": Qt.CursorShape.SizeHorCursor,
            "NE": Qt.CursorShape.SizeBDiagCursor, "SW": Qt.CursorShape.SizeBDiagCursor,
            "NW": Qt.CursorShape.SizeFDiagCursor, "SE": Qt.CursorShape.SizeFDiagCursor,
        }.get(edge, Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            edge = self._edge_at(e.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._resize_start_geo = self.geometry()
                self._resize_start_pos = e.globalPosition().toPoint()
                return
            self._drag_pos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        pos = e.position().toPoint()
        if self._resize_edge and (e.buttons() & Qt.MouseButton.LeftButton):
            delta = e.globalPosition().toPoint() - self._resize_start_pos
            g = self._resize_start_geo
            x, y, w, h = g.x(), g.y(), g.width(), g.height()
            edge = self._resize_edge
            min_w, min_h = self.minimumWidth(), self.minimumHeight()
            if "E" in edge: w = max(min_w, g.width() + delta.x())
            if "S" in edge: h = max(min_h, g.height() + delta.y())
            if "W" in edge:
                new_w = max(min_w, g.width() - delta.x())
                x = g.x() + (g.width() - new_w); w = new_w
            if "N" in edge:
                new_h = max(min_h, g.height() - delta.y())
                y = g.y() + (g.height() - new_h); h = new_h
            self.setGeometry(x, y, w, h)
            return
        edge = self._edge_at(pos)
        self.setCursor(QCursor(self._cursor_for_edge(edge)))
        if self._drag_pos is not None:
            delta = e.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = e.globalPosition().toPoint()
        self._reset_auto_hide()

    def mouseReleaseEvent(self, e):
        self._resize_edge = None
        self._drag_pos = None
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(self.stage_body.rect())
        if self.btn_reopen.isVisible():
            self._place_reopen_button()

    def closeEvent(self, event):
        if self.player is not None:
            try:
                self.player.terminate()
            except Exception:
                pass
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 9))
    w = Skyrock()
    w.show()
    sys.exit(app.exec())