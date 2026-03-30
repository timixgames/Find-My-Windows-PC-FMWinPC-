import telebot
import os
import sys
import time
import datetime
import threading
import subprocess
import psutil
import platform
import socket
import winreg
import ctypes
import ctypes.wintypes
import json
import urllib.request
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# 🔑 REPLACE THESE VALUES BEFORE FIRST RUN!
BOT_TOKEN = ('8583650760:AAEpvWIU0Al6ollo8oBSesb-w2YMkK7vXWM')  # ← Get from @BotFather
MY_USER_ID = 5427175293  # ← Get from @userinfobot

# === File paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
NIRCMD_PATH = os.path.join(SCRIPT_DIR, "nircmd.exe")
LOG_FILE = os.path.join(SCRIPT_DIR, "log.txt")
WIFI_LOG_FILE = os.path.join(SCRIPT_DIR, "last_wifi.txt")
SETTINGS_FILE = os.path.join(SCRIPT_DIR, "settings.txt")

# === Bot initialization ===
bot = telebot.TeleBot(BOT_TOKEN)

# === Global variables ===
is_searching_pc = False
was_muted_before_search = False
original_volume_level = 65535
user_action_state = {}
is_muted_global = False
current_volume_level = 65535
DANGEROUS_PROCESSES = ["wininit.exe", "winlogon.exe", "services.exe", "lsass.exe", "smss.exe", "csrss.exe",
                       "conhost.exe", "system", "registry"]
DANGEROUS_APPS = ["wininit.exe", "cmd.exe /c shutdown", "taskkill", "format", "diskpart"]

# === Localization dictionary ===
LANG = {
    "ru": {
        "first_run_title": "👋 Добро пожаловать!",
        "first_run_text": "Выберите язык интерфейса:",
        "lang_ru": "🇷🇺 Русский",
        "lang_en": "🇬🇧 English",
        "lang_changed": "✅ Язык изменён",
        "lang_button": "🌐 Язык",
        "main_menu": "📊 Система|👁️ Активность|📡 Сетевые подключения|📥 Отчёт об использовании|🚪 История входов|🖼️ Сделать скриншот|📤 Отправить лог|📁 Проекты|🔆 Яркость +|🔅 Яркость -|🔊 Громкость+|🔉 Громкость-|🔇 Вкл/Выкл звук|🚀 Запустить свою программу|🔍 Диспетчер задач|📋 Буфер обмена|🌐 Интернет|🌙 Сон|🚪 Выйти из системы|🔒 Заблокировать|🔄 Перезагрузить|⏹ Выключить|⏹ Отменить запланированное выключение или перезагрузку|📶 Статус|📍 Локатор|🔎 Найти ПК|🌐 Язык|ℹ️ Помощь",
        "system": "📊 Система",
        "activity": "👁️ Активность",
        "network": "📡 Сетевые подключения",
        "report": "📥 Отчёт об использовании",
        "logon_history": "🚪 История входов",
        "screenshot": "🖼️ Сделать скриншот",
        "send_log": "📤 Отправить лог",
        "projects": "📁 Проекты",
        "brightness_up": "🔆 Яркость +",
        "brightness_down": "🔅 Яркость -",
        "volume_up": "🔊 Громкость+",
        "volume_down": "🔉 Громкость-",
        "toggle_mute": "🔇 Вкл/Выкл звук",
        "run_app": "🚀 Запустить свою программу",
        "task_manager": "🔍 Диспетчер задач",
        "clipboard": "📋 Буфер обмена",
        "internet": "🌐 Интернет",
        "sleep": "🌙 Сон",
        "logoff": "🚪 Выйти из системы",
        "lock": "🔒 Заблокировать",
        "reboot": "🔄 Перезагрузить",
        "shutdown": "⏹ Выключить",
        "cancel_shutdown": "⏹ Отменить запланированное выключение или перезагрузку",
        "status": "📶 Статус",
        "locator": "📍 Локатор",
        "find_pc": "🔎 Найти ПК",
        "stop_script": "⏹ Остановить скрипт",
        "help": "ℹ️ Помощь",
        "back": "↩️ Назад",
        "now": "✅ Сейчас",
        "later": "🕒 Позже",
        "yes_stop": "✅ Да, остановить",
        "no": "❌ Нет",
        "stop_search": "⏹ Остановить поиск",
        "find_sound": "🔊 Найти ПК",
        "desktop": "📁 Рабочий стол",
        "downloads": "📁 Загрузки",
        "documents": "📁 Документы",
        "startup_already": "✅ уже в автозагрузке",
        "startup_added": "✅ добавлено в автозагрузку",
        "bot_starting": "✅ Бот запускается...",
        "bot_started": "✅ Бот запущен и готов к работе!",
        "greeting_sent": "✅ Приветствие отправлено!",
        "greeting_failed": "❌ Не удалось отправить приветствие",
        "new_message_title": "📩 Новое сообщение",
        "message_shown": "✅ Сообщение показано на экране ПК!",
        "error_prefix": "❌ Ошибка",
        "pc_ready": "🟢 ПК в сети и готов к работе!",
        "search_started": "🔊 Поиск запущен!\n🕒 4 звука (~20 сек).",
        "search_already": "🔍 Поиск уже активен!",
        "nircmd_missing": "❌ nircmd.exe не найден!",
        "search_stopped": "✅ Поиск остановлен!",
        "search_finished": "✅ Поиск завершён!",
        "brightness_changed": "🔆 Яркость изменена на {}%",
        "volume_changed": "🔊 Громкость изменена на {}%",
        "muted": "🔇 Звук отключён",
        "unmuted": "🔊 Звук включён",
        "active_now": "🟢 Активен (последнее действие: {} сек назад)",
        "idle_mins": "⏳ Простаивает: {} мин",
        "idle_hours": "😴 Простаивает: {} ч",
        "no_connections": "🔌 Нет активных подключений.",
        "report_title": "📥 **Отчёт об использовании ПК**",
        "ram_usage": "ОЗУ",
        "disks": "Диски",
        "network_sent": "Отпр.",
        "network_recv": "Получ.",
        "mb": "MB",
        "cpu": "CPU",
        "cores": "Ядра",
        "threads": "Потоки",
        "freq": "Частота",
        "mhz": "MHz",
        "load": "Загрузка",
        "gpu": "GPU",
        "ram": "ОЗУ",
        "battery": "🔋 Не обнаружена",
        "battery_charging": "🔌 Заряд: {}% (в сети)",
        "battery_remaining": "🔋 Заряд: {}%",
        "battery_time": "🔋 Заряд: {}%\n⏱️ Осталось: {}ч {}мин",
        "clipboard_prompt": "✏️ Отправьте текст для копирования на ПК:",
        "clipboard_copied": "✅ Текст скопирован в буфер обмена на ПК!",
        "enter_app_name": "✏️ Введите название программы (например: notepad.exe):",
        "app_forbidden": "❌ Запрещено!",
        "app_started": "✅ Запущено: {}",
        "no_processes": "❌ Процессов не найдено.",
        "processes_count": "📋 Процессов: {}. Выберите для завершения:",
        "process_killed": "✅ Завершён: {} (PID: {})",
        "internet_ok": "✅ Интернет работает!\n⏱️ Пинг: {} мс",
        "no_internet": "❌ Нет интернета.",
        "going_to_sleep": "🌙 Компьютер уходит в сон...",
        "logging_off": "🚪 Выполняется выход...",
        "pc_locked": "✅ Компьютер заблокирован!",
        "confirm_shutdown": "Выключить компьютер?",
        "confirm_reboot": "Перезагрузить компьютер?",
        "enter_time": "🕗 Введите время ЧЧ:ММ:",
        "invalid_time": "❌ Неверный формат. Пример: 01:30",
        "scheduled": "✅ Запланировано.",
        "shutdown_cancelled": "✅ Отменено!",
        "cancel_failed": "❌ Не удалось отменить",
        "logon_history_title": "✅ Последние входы в систему:",
        "no_logon_records": "ℹ️ Не найдено записей о входе в систему.",
        "location_title": "🌍 **IP**: {}\n🏙️ **Город**: {}\nреги́он: {}\nстрана́: {}\n📬 **Адрес**: {}\n🔗 [Посмотреть на карте]({})",
        "location_error": "❌ Ошибка: {}",
        "find_prompt": "🔍 Нужно найти компьютер по звуку?",
        "help_text": "✅ Возможности бота:\n— 📊 Система — информация о ПК\n— 👁️ Активность — работает ли кто-то за ПК\n— 📡 Сетевые подключения — кто использует интернет\n— 🔌 USB-устройства — подключённые устройства\n— 📥 Отчёт об использовании — сводка\n— 🚪 История входов — кто заходил в систему\n— 🖼️ Скриншот — всех мониторов\n— 📤 Лог — отправить файл лога\n— 📁 Проекты — открыть папку\n— 🔆/🔅 — яркость экрана\n— 🔊/🔉 — громкость (через nircmd)\n— 🔇 — вкл/выкл звука (через nircmd)\n— 🚀 — запуск программ\n— 🔍 — диспетчер задач\n— 📋 — копирование текста в буфер ПК\n— 🌐 — проверка интернета\n— 🌙 — сон\n— 🚪 — выход из системы\n— 🔒 — блокировка\n— 🔄/⏹ — перезагрузка/выключение\n— ⏹ Отменить — отмена запланированного\n— 📶 — статус ПК\n— 📍 — местоположение + улица/дом + поиск ПК по звуку\n— ⏹ Остановить — завершить скрипт",
        "stop_confirm": "❓ Остановить скрипт?",
        "stopping": "🛑 Скрипт останавливается...",
        "continue_working": "✅ Продолжаем работу.",
        "script_stopped": "🛑 Скрипт остановлен",
        "screenshot_caption": "✅ Скриншот всех мониторов",
        "log_caption": "📄 Файл лога",
        "log_not_found": "❌ Лог не найден.",
        "folder_not_found": "❌ Папка не найдена.",
        "folder_opened": "✅ Открыто: {}",
        "project_prompt": "📂 Выберите папку:",
        "wifi_changed": "📶 Подключено к новой Wi-Fi сети:\n`{}`",
        "new_wifi": "📶 Новая сеть: {}",
        "error_wifi_notify": "⚠️ Не удалось отправить уведомление Wi-Fi: {}",
        "error_wifi": "⚠️ Ошибка Wi-Fi: {}",
        "error_screenshot": "❌ Ошибка скриншота: {}",
        "error_log_send": "❌ Ошибка: {}",
        "error_system_info": "❌ Ошибка системной информации: {}",
        "error_activity": "❌ Ошибка: {}",
        "error_network": "❌ Ошибка: {}",
        "error_report": "❌ Ошибка: {}",
        "error_usb": "❌ Ошибка: {}",
        "error_clipboard": "❌ Ошибка: {}",
        "error_app_start": "❌ Ошибка: {}",
        "error_taskmgr": "❌ Ошибка: {}",
        "error_internet": "❌ Интернет: {}",
        "error_shutdown": "❌ Ошибка выключения: {}",
        "error_locator": "❌ Ошибка локатора: {}",
        "error_geocoding": "⚠️ Ошибка геокодирования: {}",
        "error_search": "❌ Ошибка поиска: {}",
        "error_sound_search": "❌ Ошибка звука поиска: {}",
        "error_restore_volume": "❌ Ошибка восстановления звука: {}",
        "error_startup": "⚠️ Ошибка автозагрузки: {}",
        "error_greeting": "❌ Ошибка приветствия: {}",
        "critical_error": "❌ Критическая ошибка: {}",
        "dependencies_missing": "❌ Install dependencies: pip install {}",
        "press_enter": "Press Enter to exit...",
        "nircmd_download": "⚠️ nircmd.exe not found. Download: https://www.nirsoft.net/utils/nircmd.html",
        "nircmd_place": "⚠️ Place nircmd.exe in the same folder as the script.",
        "script_manual_stop": "⏹ Скрипт остановлен вручную / Script stopped manually",
        "script_crash": "❌ Скрипт завершён с ошибкой: {} / Script crashed: {}",
    },
    "en": {
        "first_run_title": "👋 Welcome!",
        "first_run_text": "Select interface language:",
        "lang_ru": "🇷🇺 Русский",
        "lang_en": "🇬🇧 English",
        "lang_changed": "✅ Language changed",
        "lang_button": "🌐 Language",
        "main_menu": "📊 System|👁️ Activity|📡 Network connections|📥 Usage report|🚪 Login history|🖼️ Take screenshot|📤 Send log|📁 Projects|🔆 Brightness +|🔅 Brightness -|🔊 Volume+|🔉 Volume-|🔇 Mute/Unmute|🚀 Run custom app|🔍 Task Manager|📋 Clipboard|🌐 Internet|🌙 Sleep|🚪 Log off|🔒 Lock|🔄 Reboot|⏹ Shutdown|⏹ Cancel scheduled shutdown/reboot|📶 Status|📍 Locator|🔎 Find PC|🌐 Language|ℹ️ Help",
        "system": "📊 System",
        "activity": "👁️ Activity",
        "network": "📡 Network connections",
        "report": "📥 Usage report",
        "logon_history": "🚪 Login history",
        "screenshot": "🖼️ Take screenshot",
        "send_log": "📤 Send log",
        "projects": "📁 Projects",
        "brightness_up": "🔆 Brightness +",
        "brightness_down": "🔅 Brightness -",
        "volume_up": "🔊 Volume+",
        "volume_down": "🔉 Volume-",
        "toggle_mute": "🔇 Mute/Unmute",
        "run_app": "🚀 Run custom app",
        "task_manager": "🔍 Task Manager",
        "clipboard": "📋 Clipboard",
        "internet": "🌐 Internet",
        "sleep": "🌙 Sleep",
        "logoff": "🚪 Log off",
        "lock": "🔒 Lock",
        "reboot": "🔄 Reboot",
        "shutdown": "⏹ Shutdown",
        "cancel_shutdown": "⏹ Cancel scheduled shutdown/reboot",
        "status": "📶 Status",
        "locator": "📍 Locator",
        "find_pc": "🔎 Find PC",
        "stop_script": "⏹ Stop script",
        "help": "ℹ️ Help",
        "back": "↩️ Back",
        "now": "✅ Now",
        "later": "🕒 Later",
        "yes_stop": "✅ Yes, stop",
        "no": "❌ No",
        "stop_search": "⏹ Stop search",
        "find_sound": "🔊 Find PC",
        "desktop": "📁 Desktop",
        "downloads": "📁 Downloads",
        "documents": "📁 Documents",
        "startup_already": "✅ already in startup",
        "startup_added": "✅ added to startup",
        "bot_starting": "✅ Bot is starting...",
        "bot_started": "✅ Bot started and ready!",
        "greeting_sent": "✅ Greeting sent!",
        "greeting_failed": "❌ Failed to send greeting",
        "new_message_title": "📩 New message",
        "message_shown": "✅ Message shown on PC screen!",
        "error_prefix": "❌ Error",
        "pc_ready": "🟢 PC is online and ready!",
        "search_started": "🔊 Search started!\n🕒 4 sounds (~20 sec).",
        "search_already": "🔍 Search is already active!",
        "nircmd_missing": "❌ nircmd.exe not found!",
        "search_stopped": "✅ Search stopped!",
        "search_finished": "✅ Search finished!",
        "brightness_changed": "🔆 Brightness changed by {}%",
        "volume_changed": "🔊 Volume changed by {}%",
        "muted": "🔇 Sound muted",
        "unmuted": "🔊 Sound unmuted",
        "active_now": "🟢 Active (last action: {} sec ago)",
        "idle_mins": "⏳ Idle: {} min",
        "idle_hours": "😴 Idle: {} hours",
        "no_connections": "🔌 No active connections.",
        "report_title": "📥 **PC Usage Report**",
        "ram_usage": "RAM",
        "disks": "Disks",
        "network_sent": "Sent",
        "network_recv": "Received",
        "mb": "MB",
        "cpu": "CPU",
        "cores": "Cores",
        "threads": "Threads",
        "freq": "Frequency",
        "mhz": "MHz",
        "load": "Load",
        "gpu": "GPU",
        "ram": "RAM",
        "battery": "🔋 Not detected",
        "battery_charging": "🔌 Charge: {}% (on power)",
        "battery_remaining": "🔋 Charge: {}%",
        "battery_time": "🔋 Charge: {}%\n⏱️ Remaining: {}h {}min",
        "clipboard_prompt": "✏️ Send text to copy to PC clipboard:",
        "clipboard_copied": "✅ Text copied to PC clipboard!",
        "enter_app_name": "✏️ Enter app name (e.g.: notepad.exe):",
        "app_forbidden": "❌ Forbidden!",
        "app_started": "✅ Started: {}",
        "no_processes": "❌ No processes found.",
        "processes_count": "📋 Processes: {}. Select to terminate:",
        "process_killed": "✅ Terminated: {} (PID: {})",
        "internet_ok": "✅ Internet works!\n⏱️ Ping: {} ms",
        "no_internet": "❌ No internet.",
        "going_to_sleep": "🌙 PC going to sleep...",
        "logging_off": "🚪 Logging off...",
        "pc_locked": "✅ PC locked!",
        "confirm_shutdown": "Shutdown computer?",
        "confirm_reboot": "Reboot computer?",
        "enter_time": "🕗 Enter time HH:MM:",
        "invalid_time": "❌ Invalid format. Example: 01:30",
        "scheduled": "✅ Scheduled.",
        "shutdown_cancelled": "✅ Cancelled!",
        "cancel_failed": "❌ Failed to cancel",
        "logon_history_title": "✅ Recent logins:",
        "no_logon_records": "ℹ️ No login records found.",
        "location_title": "🌍 **IP**: {}\n🏙️ **City**: {}\nregion: {}\ncountry: {}\n📬 **Address**: {}\n🔗 [View on map]({})",
        "location_error": "❌ Error: {}",
        "find_prompt": "🔍 Need to find computer by sound?",
        "help_text": "✅ Bot capabilities:\n— 📊 System — PC information\n— 👁️ Activity — is someone using the PC\n— 📡 Network connections — who uses internet\n— 🔌 USB devices — connected devices\n— 📥 Usage report — summary\n— 🚪 Login history — who logged in\n— 🖼️ Screenshot — all monitors\n— 📤 Log — send log file\n— 📁 Projects — open folder\n— 🔆/🔅 — screen brightness\n— 🔊/🔉 — volume (via nircmd)\n— 🔇 — mute/unmute (via nircmd)\n— 🚀 — run apps\n— 🔍 — task manager\n— 📋 — copy text to PC clipboard\n— 🌐 — internet check\n— 🌙 — sleep\n— 🚪 — log off\n— 🔒 — lock\n— 🔄/⏹ — reboot/shutdown\n— ⏹ Cancel — cancel scheduled\n— 📶 — PC status\n— 📍 — location + street/house + find PC by sound\n— ⏹ Stop — terminate script",
        "stop_confirm": "❓ Stop the script?",
        "stopping": "🛑 Stopping script...",
        "continue_working": "✅ Continuing work.",
        "script_stopped": "🛑 Script stopped",
        "screenshot_caption": "✅ Screenshot of all monitors",
        "log_caption": "📄 Log file",
        "log_not_found": "❌ Log not found.",
        "folder_not_found": "❌ Folder not found.",
        "folder_opened": "✅ Opened: {}",
        "project_prompt": "📂 Select folder:",
        "wifi_changed": "📶 Connected to new Wi-Fi network:\n`{}`",
        "new_wifi": "📶 New network: {}",
        "error_wifi_notify": "⚠️ Failed to send Wi-Fi notification: {}",
        "error_wifi": "⚠️ Wi-Fi error: {}",
        "error_screenshot": "❌ Screenshot error: {}",
        "error_log_send": "❌ Error: {}",
        "error_system_info": "❌ System info error: {}",
        "error_activity": "❌ Error: {}",
        "error_network": "❌ Error: {}",
        "error_report": "❌ Error: {}",
        "error_usb": "❌ Error: {}",
        "error_clipboard": "❌ Error: {}",
        "error_app_start": "❌ Error: {}",
        "error_taskmgr": "❌ Error: {}",
        "error_internet": "❌ Internet: {}",
        "error_shutdown": "❌ Shutdown error: {}",
        "error_locator": "❌ Locator error: {}",
        "error_geocoding": "⚠️ Geocoding error: {}",
        "error_search": "❌ Search error: {}",
        "error_sound_search": "❌ Sound search error: {}",
        "error_restore_volume": "❌ Volume restore error: {}",
        "error_startup": "⚠️ Startup error: {}",
        "error_greeting": "❌ Greeting error: {}",
        "critical_error": "❌ Critical error: {}",
        "dependencies_missing": "❌ Install dependencies: pip install {}",
        "press_enter": "Press Enter to exit...",
        "nircmd_download": "⚠️ nircmd.exe not found. Download: https://www.nirsoft.net/utils/nircmd.html",
        "nircmd_place": "⚠️ Place nircmd.exe in the same folder as the script.",
        "script_manual_stop": "⏹ Script stopped manually / Скрипт остановлен вручную",
        "script_crash": "❌ Script crashed: {} / Скрипт завершён с ошибкой: {}",
    }
}

# === Current language (will be loaded from settings) ===
CURRENT_LANG = "en"


def load_settings():
    """Load settings from JSON file. Create default if missing."""
    global CURRENT_LANG
    default_settings = {"language": "en", "first_run": True}

    try:
        os.makedirs(SCRIPT_DIR, exist_ok=True)

        if not os.path.exists(SETTINGS_FILE):
            return default_settings

        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                settings = json.loads(content)
                CURRENT_LANG = settings.get("language", "en")
                return settings
            else:
                return default_settings
    except Exception as e:
        print(f"⚠️ Settings load error: {e}")
        CURRENT_LANG = default_settings["language"]
        return default_settings


def save_settings(settings):
    """Save settings to JSON file."""
    global CURRENT_LANG
    try:
        os.makedirs(SCRIPT_DIR, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        CURRENT_LANG = settings.get("language", CURRENT_LANG)
        print(f"✅ Settings saved: language={CURRENT_LANG}, first_run={settings.get('first_run', True)}")
    except Exception as e:
        print(f"⚠️ Settings save error: {e}")


def tr(key):
    """Get localized string by key."""
    return LANG[CURRENT_LANG].get(key, f"MISSING:{key}")


def log_event(message: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {message}"
    print(log_line)
    try:
        os.makedirs(SCRIPT_DIR, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"⚠️ Log write error: {e}")


def check_internet_quick():
    """Quick internet connectivity check"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False


def handle_bot_connection_error(error: Exception):
    """Handle bot connection errors with bilingual output"""
    error_msg = str(error)
    error_type = type(error).__name__
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 📝 Detailed log entry (technical info)
    log_event(f"❌ CRITICAL BOT CONNECTION ERROR [{timestamp}]")
    log_event(f"   Error type: {error_type}")
    log_event(f"   Error message: {error_msg}")
    log_event(f"   Token preview: {BOT_TOKEN[:10]}...{BOT_TOKEN[-4:]}")
    log_event(f"   User ID: {MY_USER_ID}")
    log_event(f"   Network check: {'OK' if check_internet_quick() else 'FAILED'}")

    # 🖥️ Console output (bilingual, user-friendly)
    print("\n" + "═" * 60)
    print("❌ ОШИБКА ЗАПУСКА БОТА / BOT STARTUP ERROR")
    print("═" * 60)
    print(f"🕒 Time: {timestamp}")
    print(f"⚠️  {error_type}: {error_msg[:100]}")
    print()

    print("🔧 ВОЗМОЖНЫЕ РЕШЕНИЯ / TROUBLESHOOTING STEPS:")
    print("─" * 60)
    print("🇷🇺 / 🇬🇧")
    print("1. Проверьте подключение к интернету")
    print("   Check your internet connection")
    print()
    print("2. Попробуйте включить/выключить VPN или прокси")
    print("   Try enabling/disabling VPN or proxy")
    print()
    print("3. Запустите диагностику сети:")
    print("   Run network diagnostics:")
    print("   → Windows: Параметры → Сеть и Интернет → Диагностика")
    print("   → Windows: Settings → Network & Internet → Troubleshoot")
    print()
    print("4. Убедитесь, что токен бота верный и не отозван")
    print("   Make sure the bot token is correct and not revoked")
    print("   → Проверьте в @BotFather / Check in @BotFather")
    print()
    print("5. Попробуйте перезапустить скрипт через 1-2 минуты")
    print("   Try restarting the script in 1-2 minutes")
    print()
    print("6. Если проблема сохраняется — обратитесь в сервисный центр")
    print("   If the problem persists — contact a service center")
    print("═" * 60)
    print(f"📄 Подробный лог: {LOG_FILE}")
    print(f"📄 Detailed log: {LOG_FILE}")
    print("═" * 60 + "\n")


def check_nircmd():
    if not os.path.exists(NIRCMD_PATH):
        log_event("❌ nircmd.exe not found")
        return False
    return True


def get_current_wifi():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, timeout=5,
            encoding='cp866', errors='ignore'
        )
        for line in result.stdout.split('\n'):
            if "SSID" in line and ":" in line:
                ssid = line.split(":")[1].strip()
                if ssid and ssid != "":
                    return ssid
    except Exception as e:
        log_event(f"⚠️ Wi-Fi error: {str(e)[:100]}")
    return None


def wifi_watcher():
    while True:
        try:
            current = get_current_wifi()
            if current:
                last = ""
                if os.path.exists(WIFI_LOG_FILE):
                    try:
                        with open(WIFI_LOG_FILE, "r", encoding="utf-8") as f:
                            last = f.read().strip()
                    except:
                        pass
                if last != current:
                    with open(WIFI_LOG_FILE, "w", encoding="utf-8") as f:
                        f.write(current)
                    try:
                        bot.send_message(
                            MY_USER_ID,
                            tr("wifi_changed").format(current),
                            parse_mode="Markdown"
                        )
                        log_event(tr("new_wifi").format(current))
                    except Exception as e:
                        log_event(tr("error_wifi_notify").format(e))
        except Exception as e:
            log_event(tr("error_wifi").format(e))
        time.sleep(30)


def show_message_window(message_text):
    """Show Windows MessageBox with 'New message' title and message text."""
    try:
        ctypes.windll.user32.MessageBoxW(0, message_text, tr("new_message_title"), 0x40 | 0x1000)
    except Exception as e:
        log_event(f"⚠️ MessageBox error: {str(e)[:100]}")


def get_idle_time_seconds():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.wintypes.UINT), ("dwTime", ctypes.wintypes.DWORD)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) // 1000


def get_system_info():
    try:
        cpu = platform.processor() or platform.machine()
        cores = psutil.cpu_count(logical=False) or 0
        threads = psutil.cpu_count(logical=True) or 0
        freq = psutil.cpu_freq().current if psutil.cpu_freq() else "N/A"
        cpu_pct = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_total = mem.total / (1024 ** 3)
        mem_used = mem.used / (1024 ** 3)

        try:
            gpu_raw = subprocess.check_output(
                ["wmic", "path", "win32_VideoController", "get", "name"],
                text=True, stderr=subprocess.DEVNULL, encoding='utf-8', errors='ignore'
            )
            gpus = [g.strip() for g in gpu_raw.split('\n') if g.strip() and g.strip() != "Name"]
            gpu = "\n".join(gpus[:2]) or "Not detected"
        except:
            gpu = "Not detected"

        disks = []
        for p in psutil.disk_partitions():
            if "cdrom" in p.opts or not p.fstype: continue
            try:
                u = psutil.disk_usage(p.mountpoint)
                free = u.free / (1024 ** 3)
                total = u.total / (1024 ** 3)
                disks.append(f"{p.device}: {free:.1f} GB / {total:.1f} GB")
            except:
                pass

        battery = tr("battery")
        b = psutil.sensors_battery()
        if b:
            p = b.percent
            if b.power_plugged:
                battery = tr("battery_charging").format(p)
            else:
                mins = b.secsleft // 60 if b.secsleft != psutil.POWER_TIME_UNLIMITED else -1
                if mins == -1:
                    battery = tr("battery_remaining").format(p)
                else:
                    battery = tr("battery_time").format(p, mins // 60, mins % 60)

        return (
                f"🖥️ **{tr('system')}**\n"
                f"**CPU**: {cpu}\n{tr('cores')}: {cores}, {tr('threads')}: {threads}\n{tr('freq')}: {freq} {tr('mhz')}\n{tr('load')}: {cpu_pct}%\n"
                f"**{tr('gpu')}**: {gpu}\n"
                f"**{tr('ram')}**: {mem_used:.1f} / {mem_total:.1f} GB ({mem.percent}%)\n"
                f"{battery}\n"
                f"**{tr('disks')}**:\n" + "\n".join(disks[:3] or ["—"])
        )
    except Exception as e:
        log_event(tr("error_system_info").format(str(e)[:100]))
        return None


def get_user_processes():
    current_pid = os.getpid()
    python_pids = {p.pid for p in psutil.process_iter() if 'python' in p.name().lower()}
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pid = p.info['pid']
            if pid in [current_pid] + list(python_pids): continue
            name = p.info['name'].lower()
            if not p.info['username'] or any(d in name for d in DANGEROUS_PROCESSES) or name in ['system', 'idle',
                                                                                                 'registry']:
                continue
            user = p.info['username'].split('\\')[-1]
            if 'system' in user.lower() or 'authority' in user.lower(): continue
            procs.append({'pid': pid, 'name': p.info['name'], 'username': user})
        except:
            continue
    return sorted(procs, key=lambda x: x['pid'])


def change_volume(percent):
    if not check_nircmd():
        return False
    try:
        value = int(65535 * (percent / 100))
        subprocess.run([NIRCMD_PATH, "changesysvolume", str(value)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception as e:
        log_event(f"Volume error: {str(e)[:100]}")
        return False


def play_search_sound(chat_id):
    global is_searching_pc
    sound = r"C:\Windows\Media\Alarm01.wav"
    try:
        import winsound
        import time as ttime
        for i in range(4):
            if not is_searching_pc: break
            winsound.PlaySound(sound, winsound.SND_FILENAME)
            if i < 3:
                ttime.sleep(1.5)
    except Exception as e:
        log_event(tr("error_sound_search").format(str(e)[:100]))
    finally:
        try:
            if check_nircmd():
                subprocess.run([NIRCMD_PATH, "setsysvolume", str(original_volume_level)], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                if was_muted_before_search:
                    subprocess.run([NIRCMD_PATH, "mutesysvolume", "1"], stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    log_event("🔇 Sound restored (muted)")
                else:
                    log_event(f"🔊 Volume restored to {original_volume_level // 655}%")
        except Exception as e:
            log_event(tr("error_restore_volume").format(str(e)[:100]))
        is_searching_pc = False
        bot.send_message(chat_id, tr("search_finished"), reply_markup=get_main_menu())


def lock_pc(): ctypes.windll.user32.LockWorkStation()


def sleep_pc(): ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)


def logoff_pc(): os.system("shutdown /l")


def add_to_startup():
    RUN_NAME = "TelegramPCControl"
    exe_path = os.path.abspath(sys.argv[0])
    command = f'"{sys.executable}" "{exe_path}"' if exe_path.endswith('.py') else f'"{exe_path}"'

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, RUN_NAME)
            winreg.CloseKey(key)
            if value == command:
                return True, tr("startup_already")
            winreg.CloseKey(key)
        except FileNotFoundError:
            winreg.CloseKey(key)

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                             winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, RUN_NAME, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        return True, tr("startup_added")
    except Exception as e:
        return False, tr("error_startup").format(str(e))


def get_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    buttons = tr("main_menu").split('|')
    for btn in buttons:
        markup.add(btn.strip())
    return markup


def get_time_choice_markup():
    m = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    m.add(tr("now"), tr("later"), tr("back"))
    return m


def get_confirm_markup():
    m = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    m.add(tr("yes_stop"), tr("no"), tr("back"))
    return m


# === First run language selection ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id != MY_USER_ID:
        return

    settings = load_settings()
    if settings.get("first_run", True):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(LANG["ru"]["lang_ru"], LANG["en"]["lang_en"])
        bot.send_message(message.chat.id, tr("first_run_text"), reply_markup=markup)
        user_action_state[MY_USER_ID] = {"action": "select_language_first_run"}
    else:
        bot.send_message(message.chat.id, tr("bot_started"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.from_user.id == MY_USER_ID and
                                    MY_USER_ID in user_action_state and
                                    user_action_state[MY_USER_ID].get("action") == "select_language_first_run")
def handle_first_run_language(message):
    global CURRENT_LANG
    if message.text == LANG["ru"]["lang_ru"]:
        CURRENT_LANG = "ru"
        settings = {"language": "ru", "first_run": False}
        save_settings(settings)
        bot.send_message(message.chat.id, f"{tr('lang_changed')} 🇷🇺 Русский", reply_markup=get_main_menu())
        log_event("$LANG Language set to Russian on first run")
    elif message.text == LANG["en"]["lang_en"]:
        CURRENT_LANG = "en"
        settings = {"language": "en", "first_run": False}
        save_settings(settings)
        bot.send_message(message.chat.id, f"{tr('lang_changed')} 🇬🇧 English", reply_markup=get_main_menu())
        log_event("$LANG Language set to English on first run")
    user_action_state.pop(MY_USER_ID, None)


# === Language change from menu ===
@bot.message_handler(func=lambda m: m.text in [LANG["ru"]["lang_button"], LANG["en"]["lang_button"]])
def handle_language_menu(message):
    if message.from_user.id != MY_USER_ID:
        return

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(LANG["ru"]["lang_ru"], LANG["en"]["lang_en"], tr("back"))
    bot.send_message(message.chat.id, tr("first_run_text"), reply_markup=markup)
    user_action_state[MY_USER_ID] = {"action": "select_language_menu"}


@bot.message_handler(func=lambda m: m.from_user.id == MY_USER_ID and
                                    MY_USER_ID in user_action_state and
                                    user_action_state[MY_USER_ID].get("action") == "select_language_menu")
def handle_menu_language(message):
    global CURRENT_LANG
    prev_lang = CURRENT_LANG

    if message.text == tr("back"):
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("continue_working"), reply_markup=get_main_menu())
        return

    if message.text == LANG["ru"]["lang_ru"]:
        CURRENT_LANG = "ru"
        settings = load_settings()
        settings["language"] = "ru"
        settings["first_run"] = False
        save_settings(settings)
        bot.send_message(message.chat.id, f"{tr('lang_changed')} 🇷🇺 Русский", reply_markup=get_main_menu())
        log_event(f"$LANG Language changed from {prev_lang} to Russian")
    elif message.text == LANG["en"]["lang_en"]:
        CURRENT_LANG = "en"
        settings = load_settings()
        settings["language"] = "en"
        settings["first_run"] = False
        save_settings(settings)
        bot.send_message(message.chat.id, f"{tr('lang_changed')} 🇬🇧 English", reply_markup=get_main_menu())
        log_event(f"$LANG Language changed from {prev_lang} to English")

    user_action_state.pop(MY_USER_ID, None)


# === Screenshot with retry on timeout ===
@bot.message_handler(func=lambda m: m.text == tr("screenshot"))
def handle_screenshot(message):
    if message.from_user.id != MY_USER_ID: return
    log_event("🖼️ Screenshot requested")
    try:
        from mss import mss
        from PIL import Image
        with mss() as sct:
            shot = sct.grab(sct.monitors[0])
            path = os.path.join(os.environ['TEMP'], "screenshot.png")
            img = Image.frombytes("RGB", shot.size, shot.rgb)
            img.save(path)

            for attempt in range(3):
                try:
                    with open(path, "rb") as f:
                        bot.send_photo(message.chat.id, f, caption=tr("screenshot_caption"),
                                       reply_markup=get_main_menu(), timeout=30)
                    break
                except Exception as e:
                    if attempt < 2:
                        time.sleep(2)
                        continue
                    raise e

            os.remove(path)
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())
        log_event(tr("error_screenshot").format(str(e)[:100]))


@bot.message_handler(func=lambda m: m.text == tr("send_log"))
def handle_send_log(message):
    if message.from_user.id != MY_USER_ID: return
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "rb") as f:
                bot.send_document(message.chat.id, f, caption=tr("log_caption"), reply_markup=get_main_menu())
        except Exception as e:
            bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, tr("log_not_found"), reply_markup=get_main_menu())


PROJECT_FOLDERS = {
    "ru": {
        "📁 Рабочий стол": os.path.expanduser("~/Desktop"),
        "📁 Загрузки": os.path.expanduser("~/Downloads"),
        "📁 Документы": os.path.expanduser("~/Documents"),
    },
    "en": {
        "📁 Desktop": os.path.expanduser("~/Desktop"),
        "📁 Downloads": os.path.expanduser("~/Downloads"),
        "📁 Documents": os.path.expanduser("~/Documents"),
    }
}


@bot.message_handler(func=lambda m: m.text == tr("projects"))
def handle_projects_menu(message):
    if message.from_user.id != MY_USER_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in PROJECT_FOLDERS[CURRENT_LANG]: markup.add(name)
    markup.add(tr("back"))
    bot.send_message(message.chat.id, tr("project_prompt"), reply_markup=markup)
    user_action_state[MY_USER_ID] = {"action": "open_project_folder"}


@bot.message_handler(func=lambda m: MY_USER_ID in user_action_state and
                                    user_action_state[MY_USER_ID].get("action") == "open_project_folder" and
                                    m.text in PROJECT_FOLDERS[CURRENT_LANG])
def open_selected_folder(message):
    if message.from_user.id != MY_USER_ID: return
    path = PROJECT_FOLDERS[CURRENT_LANG][message.text]
    user_action_state.pop(MY_USER_ID, None)
    if os.path.exists(path):
        try:
            os.startfile(path)
            bot.send_message(message.chat.id, tr("folder_opened").format(message.text), reply_markup=get_main_menu())
            log_event(f"📁 Folder opened: {path}")
        except Exception as e:
            bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())
    else:
        bot.send_message(message.chat.id, tr("folder_not_found"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text in [tr("brightness_up"), tr("brightness_down")])
def adjust_brightness(message):
    if message.from_user.id != MY_USER_ID: return
    if not check_nircmd():
        bot.send_message(message.chat.id, tr("nircmd_missing"), reply_markup=get_main_menu())
        return
    step = 10 if message.text == tr("brightness_up") else -10
    try:
        subprocess.run([NIRCMD_PATH, "changebrightness", str(step)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        bot.send_message(message.chat.id, tr("brightness_changed").format(abs(step)), reply_markup=get_main_menu())
        log_event(f"🔆 Brightness {'increased' if step > 0 else 'decreased'} by {abs(step)}%")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text in [tr("volume_up"), tr("volume_down")])
def adjust_volume(message):
    if message.from_user.id != MY_USER_ID: return
    if not check_nircmd():
        bot.send_message(message.chat.id, tr("nircmd_missing"), reply_markup=get_main_menu())
        return
    step = 10 if message.text == tr("volume_up") else -10
    try:
        change_volume(step if step > 0 else step)
        bot.send_message(message.chat.id, tr("volume_changed").format(abs(step)), reply_markup=get_main_menu())
        log_event(f"🔊 Volume {'increased' if step > 0 else 'decreased'} by {abs(step)}%")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("toggle_mute"))
def toggle_mute(message):
    global is_muted_global, current_volume_level
    if message.from_user.id != MY_USER_ID: return
    if not check_nircmd():
        bot.send_message(message.chat.id, tr("nircmd_missing"), reply_markup=get_main_menu())
        return
    try:
        if not is_muted_global:
            current_volume_level = 65535
            subprocess.run([NIRCMD_PATH, "mutesysvolume", "1"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            is_muted_global = True
            bot.send_message(message.chat.id, tr("muted"), reply_markup=get_main_menu())
            log_event("🔇 Sound muted")
        else:
            subprocess.run([NIRCMD_PATH, "mutesysvolume", "0"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            is_muted_global = False
            bot.send_message(message.chat.id, tr("unmuted"), reply_markup=get_main_menu())
            log_event("🔊 Sound unmuted")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("activity"))
def handle_activity_check(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        idle = get_idle_time_seconds()
        if idle < 60:
            msg = tr("active_now").format(idle)
        elif idle < 3600:
            msg = tr("idle_mins").format(idle // 60)
        else:
            msg = tr("idle_hours").format(idle // 3600)
        bot.send_message(message.chat.id, msg, reply_markup=get_main_menu())
        log_event("👁️ Activity checked")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("network"))
def handle_net_connections(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        conns = [c for c in psutil.net_connections(kind='inet') if c.status == 'ESTABLISHED' and c.raddr and c.pid]
        lines = [f"📡 **{tr('network')}**:\n"]
        for c in conns[:15]:
            try:
                name = psutil.Process(c.pid).name()
                lines.append(f"• `{name}` → {c.raddr.ip}:{c.raddr.port}")
            except:
                continue
        if len(lines) == 1:
            bot.send_message(message.chat.id, tr("no_connections"), reply_markup=get_main_menu())
        else:
            bot.send_message(message.chat.id, "\n".join(lines), parse_mode="Markdown", reply_markup=get_main_menu())
        log_event("📡 Network connections checked")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("report"))
def handle_usage_report(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        idle = get_idle_time_seconds()
        activity = "🟢 " + (tr("active_now").format(5) if idle < 60 else tr("idle_mins").format(idle // 60))
        disks = []
        for p in psutil.disk_partitions():
            if 'cdrom' in p.opts or not p.fstype: continue
            try:
                u = psutil.disk_usage(p.mountpoint)
                disks.append(f"{p.device}: {u.free / (1024 ** 3):.1f} GB free")
            except:
                pass
        mem = psutil.virtual_memory()
        net = psutil.net_io_counters()
        report = (
                f"{tr('report_title')}\n"
                f"**Activity:** {activity}\n"
                f"**{tr('ram_usage')}**: {mem.percent}%\n"
                f"**{tr('disks')}**:\n" + "\n".join(disks[:2] or ["—"]) + "\n"
                                                                          f"**Network:**\n{tr('network_sent')}: {net.bytes_sent / (1024 ** 2):.1f} {tr('mb')}\n{tr('network_recv')}: {net.bytes_recv / (1024 ** 2):.1f} {tr('mb')}"
        )
        bot.send_message(message.chat.id, report, parse_mode="Markdown", reply_markup=get_main_menu())
        log_event("📥 Usage report")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("system"))
def handle_system_info(message):
    if message.from_user.id != MY_USER_ID: return
    info = get_system_info()
    bot.send_message(message.chat.id, info or f"{tr('error_prefix')}!", parse_mode="Markdown" if info else None,
                     reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("clipboard"))
def handle_clipboard_start(message):
    if message.from_user.id != MY_USER_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(tr("back"))
    bot.send_message(message.chat.id, tr("clipboard_prompt"), reply_markup=markup)
    user_action_state[MY_USER_ID] = {"action": "clipboard"}


@bot.message_handler(
    func=lambda m: MY_USER_ID in user_action_state and user_action_state[MY_USER_ID].get("action") == "clipboard")
def handle_clipboard_text(message):
    if message.from_user.id != MY_USER_ID: return
    if message.text == tr("back"):
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("back"), reply_markup=get_main_menu())
        return
    try:
        import pyperclip
        pyperclip.copy(message.text)
        bot.send_message(message.chat.id, tr("clipboard_copied"), reply_markup=get_main_menu())
        log_event(f"📋 Copied {len(message.text)} chars")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:100]}", reply_markup=get_main_menu())
    user_action_state.pop(MY_USER_ID, None)


@bot.message_handler(func=lambda m: m.text == tr("run_app"))
def handle_custom_app_start(message):
    if message.from_user.id != MY_USER_ID: return
    bot.send_message(message.chat.id, tr("enter_app_name"), reply_markup=get_main_menu())
    user_action_state[MY_USER_ID] = {"action": "run_custom_app"}


@bot.message_handler(
    func=lambda m: MY_USER_ID in user_action_state and user_action_state[MY_USER_ID].get("action") == "run_custom_app")
def handle_custom_app_name(message):
    if message.from_user.id != MY_USER_ID: return
    app = message.text.strip().lower()
    if any(d in app for d in DANGEROUS_APPS) or app in DANGEROUS_PROCESSES:
        bot.send_message(message.chat.id, tr("app_forbidden"), reply_markup=get_main_menu())
        user_action_state.pop(MY_USER_ID, None)
        return
    try:
        p = subprocess.Popen(app, shell=True)
        bot.send_message(message.chat.id, tr("app_started").format(app), reply_markup=get_main_menu())
        log_event(f"🚀 Started: {app} (PID: {p.pid})")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())
    user_action_state.pop(MY_USER_ID, None)


@bot.message_handler(func=lambda m: m.text == tr("task_manager"))
def handle_task_manager(message):
    if message.from_user.id != MY_USER_ID: return
    procs = get_user_processes()
    if not procs:
        bot.send_message(message.chat.id, tr("no_processes"), reply_markup=get_main_menu())
        return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for p in procs[:20]:
        markup.add(f"{p['name']} (PID: {p['pid']})")
    markup.add(tr("back"))
    bot.send_message(message.chat.id, tr("processes_count").format(len(procs)), reply_markup=markup)
    user_action_state[MY_USER_ID] = {"action": "kill_process", "processes": {p['pid']: p for p in procs}}


@bot.message_handler(
    func=lambda m: MY_USER_ID in user_action_state and user_action_state[MY_USER_ID].get("action") == "kill_process")
def handle_kill_process(message):
    if message.from_user.id != MY_USER_ID: return
    if message.text == tr("back"):
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("back"), reply_markup=get_main_menu())
        return
    try:
        if "(PID: " in message.text:
            pid = int(message.text.split("(PID: ")[1].split(")")[0])
        else:
            pid = int(message.text)
        procs = user_action_state[MY_USER_ID].get("processes", {})
        if pid not in procs:
            raise ValueError("Process not found")
        p = psutil.Process(pid)
        p.terminate()
        p.wait(timeout=3)
        bot.send_message(message.chat.id, tr("process_killed").format(procs[pid]['name'], pid),
                         reply_markup=get_main_menu())
        log_event(f"🔍 Terminated PID: {pid}")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())
    user_action_state.pop(MY_USER_ID, None)


@bot.message_handler(func=lambda m: m.text == tr("internet"))
def handle_internet_check(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        start = datetime.datetime.now()
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        ping = (datetime.datetime.now() - start).total_seconds() * 1000
        bot.send_message(message.chat.id, tr("internet_ok").format(int(ping)), reply_markup=get_main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, tr("no_internet"), reply_markup=get_main_menu())
        log_event(tr("error_internet").format(str(e)[:100]))


@bot.message_handler(func=lambda m: m.text == tr("sleep"))
def handle_sleep(message):
    if message.from_user.id != MY_USER_ID: return
    log_event("🌙 Sleep")
    bot.send_message(message.chat.id, tr("going_to_sleep"), reply_markup=get_main_menu())
    threading.Thread(target=sleep_pc, daemon=True).start()


@bot.message_handler(func=lambda m: m.text == tr("logoff"))
def handle_logoff(message):
    if message.from_user.id != MY_USER_ID: return
    log_event("🚪 Logoff")
    bot.send_message(message.chat.id, tr("logging_off"), reply_markup=get_main_menu())
    threading.Thread(target=logoff_pc, daemon=True).start()


@bot.message_handler(func=lambda m: m.text == tr("lock"))
def handle_lock(message):
    if message.from_user.id != MY_USER_ID: return
    log_event("🔒 Lock")
    lock_pc()
    bot.send_message(message.chat.id, tr("pc_locked"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text in [tr("reboot"), tr("shutdown")])
def handle_shutdown_reboot_choice(message):
    if message.from_user.id != MY_USER_ID: return
    action = "reboot" if message.text == tr("reboot") else "shutdown"
    log_event(f"🔄/⏹ {'Reboot' if action == 'reboot' else 'Shutdown'}")
    user_action_state[MY_USER_ID] = {"action": action}
    prompt = tr("confirm_reboot") if action == "reboot" else tr("confirm_shutdown")
    bot.send_message(message.chat.id, prompt, reply_markup=get_time_choice_markup())


@bot.message_handler(func=lambda m: m.text in [tr("now"), tr("later"), tr("back")])
def handle_time_choice(message):
    if message.from_user.id != MY_USER_ID or MY_USER_ID not in user_action_state: return
    if message.text == tr("back"):
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("back"), reply_markup=get_main_menu())
        return
    action = user_action_state[MY_USER_ID]["action"]
    if message.text == tr("now"):
        cmd = "shutdown /r /t 0" if action == "reboot" else "shutdown /s /t 0"
        os.system(cmd)
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("scheduled"), reply_markup=get_main_menu())
    else:
        user_action_state[MY_USER_ID]["step"] = "waiting_time"
        bot.send_message(message.chat.id, tr("enter_time"))


@bot.message_handler(
    func=lambda m: MY_USER_ID in user_action_state and user_action_state[MY_USER_ID].get("step") == "waiting_time")
def handle_time_input(message):
    if message.from_user.id != MY_USER_ID: return
    if message.text == tr("back"):
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("back"), reply_markup=get_main_menu())
        return
    try:
        hh, mm = message.text.strip().split(':')
        total = int(hh) * 3600 + int(mm) * 60
        if total == 0 or total > 86400:
            raise ValueError
        action = user_action_state[MY_USER_ID]["action"]
        os.system(f"shutdown /{'r' if action == 'reboot' else 's'} /t {total}")
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("scheduled"), reply_markup=get_main_menu())
    except:
        bot.send_message(message.chat.id, tr("invalid_time"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("cancel_shutdown"))
def cancel_shutdown(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        os.system("shutdown /a")
        bot.send_message(message.chat.id, tr("shutdown_cancelled"), reply_markup=get_main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('cancel_failed')}: {str(e)[:80]}", reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("status"))
def handle_status(message):
    if message.from_user.id != MY_USER_ID: return
    bot.send_message(message.chat.id, tr("pc_ready"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("logon_history"))
def handle_logon_history(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        cmd = '''
$events = Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624} -MaxEvents 10 -ErrorAction SilentlyContinue
foreach ($e in $events) {
$xml = [xml]$e.ToXml()
$user = $xml.Event.EventData.Data | Where-Object {$_.Name -eq "TargetUserName"} | Select-Object -ExpandProperty "#text"
$domain = $xml.Event.EventData.Data | Where-Object {$_.Name -eq "TargetDomainName"} | Select-Object -ExpandProperty "#text"
$time = $e.TimeCreated.ToString("yyyy-MM-dd HH:mm")
"$time | $domain\\$user"
}
'''
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore'
        )
        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        if lines:
            text = tr("logon_history_title") + "\n" + "\n".join(f"• {line}" for line in lines)
        else:
            text = tr("no_logon_records")
        bot.send_message(message.chat.id, text, reply_markup=get_main_menu())
        log_event("🚪 Login history requested")
    except Exception as e:
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:100]}", reply_markup=get_main_menu())


# === Locator ===
@bot.message_handler(func=lambda m: m.text == tr("locator"))
def handle_location_request(message):
    if message.from_user.id != MY_USER_ID: return
    try:
        with urllib.request.urlopen("https://ipinfo.io/json", timeout=10) as response:
            data = json.loads(response.read())
        ip = data.get('ip', 'unknown')
        city = data.get('city', '—')
        region = data.get('region', '—')
        country = data.get('country', '—')
        loc = data.get('loc')
        full_address = "❌ Exact address unavailable"
        google_maps_link = "#"
        if loc:
            lat, lon = loc.split(',')
            google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            try:
                nominatim_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language={'ru' if CURRENT_LANG == 'ru' else 'en'}"
                req = urllib.request.Request(
                    nominatim_url,
                    headers={'User-Agent': 'TelegramPCControl/1.0 (your-email@example.com)'}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    addr_data = json.loads(resp.read())
                    if 'address' in addr_data:
                        addr = addr_data['address']
                        house = addr.get('house_number', '').strip()
                        street = (addr.get('road') or addr.get('pedestrian') or addr.get('path') or '').strip()
                        if street and house:
                            full_address = f"{street}, {house}"
                        elif house and not street:
                            suburb = addr.get('suburb', addr.get('neighbourhood', ''))
                            if suburb:
                                full_address = f"{suburb}, house {house}"
                            else:
                                full_address = f"House {house}"
                        elif street and not house:
                            full_address = f"{street} (house number not specified)"
                        else:
                            full_address = "📍 Address not recognized"
                    else:
                        full_address = "📍 Address unavailable"
            except Exception as e:
                log_event(tr("error_geocoding").format(str(e)[:100]))
        loc_text = tr("location_title").format(ip, city, region, country, full_address, google_maps_link)
        bot.send_message(message.chat.id, loc_text, parse_mode="Markdown", disable_web_page_preview=True)
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        markup.add(tr("find_sound"))
        markup.add(tr("back"))
        bot.send_message(message.chat.id, tr("find_prompt"), reply_markup=markup)
        user_action_state[MY_USER_ID] = {"action": "in_locator_menu"}
    except Exception as e:
        bot.send_message(message.chat.id, tr("location_error").format(str(e)[:100]), reply_markup=get_main_menu())
        log_event(tr("error_locator").format(str(e)[:150]))


@bot.message_handler(func=lambda m: m.text == tr("find_sound") and
                                    MY_USER_ID in user_action_state and
                                    user_action_state[MY_USER_ID].get("action") == "in_locator_menu")
def handle_find_pc_from_locator(message):
    handle_find_pc(message)


@bot.message_handler(func=lambda m: m.text == tr("back") and
                                    MY_USER_ID in user_action_state and
                                    user_action_state[MY_USER_ID].get("action") == "in_locator_menu")
def back_from_locator(message):
    user_action_state.pop(MY_USER_ID, None)
    bot.send_message(message.chat.id, tr("back"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("find_pc"))
def handle_find_pc(message):
    global is_searching_pc, was_muted_before_search, original_volume_level
    if message.from_user.id != MY_USER_ID: return
    if is_searching_pc:
        bot.send_message(message.chat.id, tr("search_already"), reply_markup=get_main_menu())
        return
    if not check_nircmd():
        bot.send_message(message.chat.id, tr("nircmd_missing"), reply_markup=get_main_menu())
        return
    log_event("🔍 PC search started")
    try:
        original_volume_level = 65535
        was_muted_before_search = False
        subprocess.run([NIRCMD_PATH, "setsysvolume", "65535"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([NIRCMD_PATH, "mutesysvolume", "0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        is_searching_pc = True
        th = threading.Thread(target=play_search_sound, args=(message.chat.id,), daemon=True)
        th.start()
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(tr("stop_search"))
        markup.add(tr("back"))
        bot.send_message(message.chat.id, tr("search_started"), reply_markup=markup)
    except Exception as e:
        is_searching_pc = False
        bot.send_message(message.chat.id, f"{tr('error_prefix')}: {str(e)[:80]}", reply_markup=get_main_menu())
        log_event(tr("error_search").format(str(e)[:100]))


@bot.message_handler(func=lambda m: m.text == tr("stop_search"))
def stop_find_pc(message):
    global is_searching_pc
    if message.from_user.id != MY_USER_ID: return
    if not is_searching_pc:
        bot.send_message(message.chat.id, "🔍 Search not active.", reply_markup=get_main_menu())
        return
    is_searching_pc = False
    bot.send_message(message.chat.id, tr("search_stopped"), reply_markup=get_main_menu())
    log_event("🔍 Search stopped")


@bot.message_handler(func=lambda m: m.text == tr("stop_script"))
def request_shutdown(message):
    if message.from_user.id != MY_USER_ID: return
    bot.send_message(message.chat.id, tr("stop_confirm"), reply_markup=get_confirm_markup())
    user_action_state[MY_USER_ID] = {"action": "stop_bot"}


@bot.message_handler(func=lambda m: m.text in [tr("yes_stop"), tr("no"), tr("back")])
def confirm_shutdown(message):
    if message.from_user.id != MY_USER_ID or user_action_state.get(MY_USER_ID, {}).get("action") != "stop_bot": return
    if message.text == tr("yes_stop"):
        log_event(tr("script_stopped"))
        bot.send_message(message.chat.id, tr("stopping"))
        threading.Timer(1.0, lambda: os._exit(0)).start()
    else:
        user_action_state.pop(MY_USER_ID, None)
        bot.send_message(message.chat.id, tr("continue_working"), reply_markup=get_main_menu())


@bot.message_handler(func=lambda m: m.text == tr("help"))
def handle_help(message):
    if message.from_user.id != MY_USER_ID: return
    bot.send_message(message.chat.id, tr("help_text"), reply_markup=get_main_menu())


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.from_user.id != MY_USER_ID:
        return

    system_commands = set(tr(key) for key in [
        "now", "later", "back", "yes_stop", "no", "stop_search",
        "desktop", "downloads", "documents",
        "system", "activity", "network", "report", "logon_history",
        "screenshot", "send_log", "projects", "brightness_up", "brightness_down",
        "volume_up", "volume_down", "toggle_mute", "run_app", "task_manager",
        "clipboard", "internet", "sleep", "logoff", "lock", "reboot", "shutdown",
        "cancel_shutdown", "status", "locator", "find_sound", "find_pc",
        "stop_script", "help", "lang_button"
    ])

    if message.text in system_commands:
        return

    log_event(f"📥 Message received: {message.text[:50]}")

    text_preview = message.text[:500] if len(message.text) <= 500 else message.text[:497] + "..."

    threading.Thread(
        target=show_message_window,
        args=(text_preview,),
        daemon=True
    ).start()

    bot.reply_to(message, tr("message_shown"), reply_markup=get_main_menu())


# === MAIN ===
if __name__ == '__main__':
    print("✅ Loading settings...")
    settings = load_settings()
    CURRENT_LANG = settings.get("language", "en")
    first_run = settings.get("first_run", True)

    print(f"🌐 Current language: {CURRENT_LANG}")
    print(f"🆕 First run: {first_run}")

    # Проверка зависимостей
    required = [('psutil', 'psutil'), ('mss', 'mss'), ('PIL', 'pillow'), ('pyperclip', 'pyperclip')]
    missing = []
    for mod, pkg in required:
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(tr("dependencies_missing").format(' '.join(missing)))
        input(tr("press_enter"))
        sys.exit(1)

    if not check_nircmd():
        print(tr("nircmd_download"))
        print(tr("nircmd_place"))

    success, status = add_to_startup()
    startup_msg = status
    print(startup_msg)
    log_event(startup_msg)

    threading.Thread(target=wifi_watcher, daemon=True).start()

    print(tr("bot_starting"))

    # 🚀 Попытка инициализации и запуска бота с обработкой ошибок
    try:
        # Проверка токена (ПРЕДУПРЕЖДЕНИЕ, но не блокировка)
        if not BOT_TOKEN or BOT_TOKEN.startswith('8583650760:AAEpvWIU0Al6ollo8oBSesb-w2YMkK7vXWM'):
            print("\n⚠️  WARNING / ПРЕДУПРЕЖДЕНИЕ:")
            print("   BOT_TOKEN не заменён! Замените токен от @BotFather")
            print("   BOT_TOKEN not replaced! Replace with token from @BotFather")
            print("   Continuing anyway to show proper error handling...\n")
            log_event("⚠️ WARNING: Placeholder token detected")

        # Тестовое подключение к API
        bot.get_me()
        print("✅ Bot API connection successful")

    except Exception as init_error:
        handle_bot_connection_error(init_error)
        input("Press Enter to exit... / Нажмите Enter для выхода...")
        sys.exit(1)

    # Отправка приветствия
    if first_run:
        print("🆕 First run detected — sending language selection...")
        try:
            bot.send_message(MY_USER_ID, "/start")
            print("✅ /start command sent")
        except Exception as e:
            print(f"⚠️ Failed to auto-send /start: {e}")
            print("💡 Open bot in Telegram and press /start manually")
    else:
        for attempt in range(3):
            try:
                bot.send_message(
                    MY_USER_ID,
                    f"🟢 PC & bot started!\n{startup_msg}",
                    reply_markup=get_main_menu()
                )
                print(tr("greeting_sent"))
                break
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1}/3: {e}")
                if attempt < 2:
                    time.sleep(3)
                else:
                    print(tr("greeting_failed"))
                    log_event(tr("error_greeting").format(e))

    print(tr("bot_started"))

    # 🔄 Запуск polling с обработкой критических ошибок
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=5)
    except KeyboardInterrupt:
        print(f"\n{tr('script_manual_stop')}")
        log_event(tr("script_manual_stop"))
    except telebot.apihelper.ApiTelegramException as e:
        log_event(f"❌ Telegram API Error: {e}")
        handle_bot_connection_error(e)
        input("Press Enter to exit... / Нажмите Enter для выхода...")
    except ConnectionError as e:
        log_event(f"❌ Connection Error: {e}")
        handle_bot_connection_error(e)
        input("Press Enter to exit... / Нажмите Enter для выхода...")
    except Exception as e:
        print(tr("script_crash").format(e))
        log_event(tr("critical_error").format(e))
        handle_bot_connection_error(e)
        input(tr("press_enter"))