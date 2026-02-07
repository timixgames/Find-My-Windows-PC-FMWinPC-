




# Control your Windows PC remotely via Telegram with a beautiful multilingual interface. Monitor system resources, manage applications, take screenshots, track location, and much more — all from your smartphone!
# ✨ Features
# 📊 System Monitoring
Real-time CPU, RAM, GPU, and disk usage statistics

Battery status with estimated remaining battery life

Network activity monitoring (active connections)

Idle time estimator (user activity)
# 🎮 Remote Control
Instant screenshot of all monitors

Application Management: Launch your own programs, end processes via Task Manager

Power Management: Sleep, Lock, Logout, Restart, Shutdown (with scheduling)

Screen Brightness Adjustment

Volume Control: Mute, Increase/Decrease volume

Clipboard Sync: Copy text from your phone to your PC's clipboard
# 🌐 Communications and Security
Wi-Fi Monitoring: Notifications when your PC connects to new networks

Geolocation: View your PC's current location with street/house number (via OpenStreetMap)

Discovery USB devices (optional)

Login history: View Windows security logs

Find PC by sound: Play a sound to physically locate your computer

# 🌍 Multi-language support Russian / English
Language selection persists across restarts

All messages are displayed in system windows with the title "📩 New message"
# 🔒 Privacy and security
Single-user access: Only your Telegram ID can control your PC

No cloud storage: All data remains on your local computer

No background telemetry: Zero data collection

# ⚠️ Required for volume/brightness control
Download from the official website: https://www.nirsoft.net/utils/nircmd.html

Unzip nircmd.exe to the same folder as FMWinPC.py

# 🔑 REPLACE THESE VALUES BEFORE THE FIRST START!
BOT_TOKEN = 'YOUR_TOKEN_HERE' # ← Get from @BotFather

MY_USER_ID = 123456789 # ← Get from @userinfobot

How to get these values:

Message @BotFather in Telegram → /newbot → follow the instructions → copy the token

Message @userinfobot → copy your ID


# On first launch:
The bot will automatically send a language selection (/start command)

Select 🇷🇺 Russian or English

The settings will be saved in settings.txt for subsequent launches

The bot will send a confirmation with a full control menu


# 🚨 Troubleshooting
Common issues and solutions

# DLL load failed while importing _ctypes
Install Visual C++ Redistributable → restart PC

# Error 409: Conflict
Close all Python processes → wait 60 seconds → restart the bot (only one instance per token is allowed)

# nircmd.exe not found
Download from NirSoft → place it in the script folder

# WMIC not found (Windows 11)
The bot automatically switches to PowerShell/CIM - no further action required

# The bot does not start after reboot
Check your antivirus quarantine → add Python to the exceptions

# Connection aborted errors
Configure a proxy or check your internet connection

# Required Windows Components
Make sure the following Windows components are enabled:

PowerShell 5.1+ (enabled by default)

Windows Management Instrumentation (WMI) (for system information)

Location Services (for geolocation)

# 💡 How to enable WMI:
Control Panel → Programs → Turn Windows features on or off → Check "Windows Management Instrumentation (WMI)"

# 🌍 Localization support
The bot supports two languages ​​with a fully translated interface: Russian and English.

Change the language at any time:

Open the bot menu

Click 🌐 Language

Select your preferred language

The settings will be saved immediately in settings.txt

# 🙏 Required components

PyTelegramBotAPI - Framework for Telegram bots (install: Windows Terminal - pip install PyTelegramBotAPI)

NirCmd - System management utility by Nir Sofer (install: download the archive from https://www.nirsoft.net/utils/nircmd.html and copy ALL files from it)

psutil - Retrieves information about computer specifications (install: Windows) Terminal - pip install psutil)

mss - Takes a screenshot of all monitors (install: Windows Terminal - pip install mss)

pillow - Sends a screenshot taken by the mss library (install: Windows Terminal - pip install pillow)

pyperclip - Copies text sent by the bot user to the computer (install: Windows Terminal - pip install pyperclip)

OpenStreetMap - Geocoding services

@BotFather & @userinfobot - Telegram bot infrastructure

# 💬 Support
Having problems? Open a GitHub Issue specifying:

Windows versions (winver in the command line)

Python versions (python --version)

Full error log from the console

Steps to reproduce the problem (if you have programming experience)

Or

Contact the bot: https://t.me/Timix_support_bot





# Управляйте своим ПК с Windows удаленно через Telegram с красивым многоязычным интерфейсом. Мониторинг ресурсов системы, управление приложениями, скриншоты, отслеживание местоположения и многое другое — всё с вашего смартфона!
# ✨ Возможности
# 📊 Мониторинг системы
Статистика загрузки процессора, оперативной памяти, видеокарты и дисков в реальном времени

Статус батареи с оценкой оставшегося времени

Мониторинг сетевой активности (активные подключения)

Определение времени простоя (активность пользователя)

# 🎮 Удаленное управление
Скриншот всех мониторов мгновенно

Управление приложениями: запуск своих программ, завершение процессов через Диспетчер задач

Управление питанием: Сон, Блокировка, Выход из системы, Перезагрузка, Выключение (с планированием)

Регулировка яркости экрана

Управление громкостью: вкл/выкл звук, увеличение/уменьшение громкости

Синхронизация буфера обмена: копирование текста с телефона в буфер ПК
# 🌐 Связь и безопасность
Мониторинг Wi-Fi: уведомления при подключении ПК к новым сетям

Геолокация: просмотр текущего местоположения ПК с указанием улицы/дома (через OpenStreetMap)

Обнаружение USB-устройств (опционально)

История входов: просмотр журналов безопасности Windows

Поиск ПК по звуку: воспроизведение звукового сигнала для физического поиска компьютера
# 🌍 Поддержка нескольких языков: Русский / English

Выбор языка сохраняется между перезапусками

Все сообщения отображаются в системных окнах с заголовком «📩 Новое сообщение»
# 🔒 Приватность и безопасность
Доступ только для одного пользователя: только ваш Telegram ID может управлять ПК

Нет облачного хранения: все данные остаются на вашем локальном компьютере

Нет фоновой телеметрии

# ⚠️ Требуется для управления громкостью/яркостью
Скачайте с официального сайта: https://www.nirsoft.net/utils/nircmd.html

Распакуйте nircmd.exe в ту же папку, где находится FMWinPC.py

# 🔑 ЗАМЕНИТЕ ЭТИ ЗНАЧЕНИЯ ПЕРЕД ПЕРВЫМ ЗАПУСКОМ!
BOT_TOKEN = 'YOUR_TOKEN_HERE'  # ← Получите у @BotFather

MY_USER_ID = 123456789          # ← Получите у @userinfobot

Как получить эти значения:

Напишите @BotFather в Telegram → /newbot → следуйте инструкциям → скопируйте токен

Напишите @userinfobot → скопируйте ваш ID

# При первом запуске:
Бот автоматически отправит выбор языка (команда /start)

Выберите Русский или English

Настройки сохранятся в settings.txt для последующих запусков

Бот отправит подтверждение с полным меню управления

# 🚨 Устранение неполадок
Распространенные проблемы и решения

# DLL load failed while importing _ctypes
Установите Visual C++ Redistributable → перезагрузите ПК

# Ошибка 409: Conflict
Закройте все процессы Python → подождите 60 сек → перезапустите бота (разрешен только один экземпляр на токен)

# nircmd.exe не найден
Скачайте с NirSoft → поместите в папку со скриптом

# WMIC не найден (Windows 11)
Бот автоматически переключается на PowerShell/CIM — дополнительных действий не требуется

# Бот не запускается после перезагрузки
Проверьте карантин антивируса → добавьте Python в исключения

# Ошибки Connection aborted
Настройте прокси или проверьте подключение к интернету

# Требуемые компоненты Windows
Убедитесь, что включены следующие компоненты Windows:

PowerShell 5.1+ (включен по умолчанию)

Среда управления Windows (WMI) (для информации о системе)

Службы определения местоположения (для функции геолокации)

# 💡 Как включить WMI:
Панель управления → Программы → Включение или отключение компонентов Windows → Отметьте "Среда управления Windows (WMI)"

# 🌍 Поддержка локализации (Localization support)
Бот поддерживает два языка с полным переводом интерфейса: Русский (Russian) и Английский (English)

Изменить язык в любое время:

Откройте меню бота

Нажмите 🌐 Язык / 🌐 Language

Выберите предпочитаемый язык

Настройки сохранятся немедленно в settings.txt

# 🙏 Необходимые компоненты

PyTelegramBotAPI - Фреймворк для Telegram ботов (установить: Windows Терминал - pip install PyTelegramBotAPI)

NirCmd - Системная утилита управления от Nir Sofer (установить: скачать архив с https://www.nirsoft.net/utils/nircmd.html и перенести из него ВСЕ файлы)

psutil - Получает информацию о характеристиках компьютера (установить: Windows Терминал - pip install psutil)

mss - Делает скриншот всех мониторов (установить: Windows Терминал - pip install mss)

pillow - Отправляет скриншот, который сделан библиотекой mss (установить: Windows Терминал - pip install pillow)

pyperclip - копирует текст, отправленный пользователем бота на компьютер (установить: Windows Терминал - pip install pyperclip)

OpenStreetMap - Сервисы геокодирования

@BotFather & @userinfobot - Инфраструктура ботов Telegram

# 💬 Поддержка
Возникли проблемы? Откройте GitHub Issue с указанием:

Версии Windows (winver в командной строке)

Версии Python (python --version)

Полного лога ошибок из консоли

Шагов для воспроизведения проблемы (если вы разбираетесь в программировании)

Или

Пишите в бота: https://t.me/Timix_support_bot
