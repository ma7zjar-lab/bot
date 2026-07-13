# ==============================
# Discord Bot Configuration
# ==============================


import os


# ==============================
# TOKEN
# ==============================

TOKEN = os.getenv("TOKEN")


# ==============================
# OWNER / ACCESS CONTROL
# ==============================

# Only these Discord IDs can use locked commands

OWNER_IDS = {
    972434666948808724,
}


# ==============================
# COMMAND SETTINGS
# ==============================

PREFIX = "!"

SLASH_COMMANDS = True
PREFIX_COMMANDS = True

SYNC_COMMANDS_ON_START = True


# ==============================
# DATABASE
# ==============================

DATABASE = "data/bot.db"


# ==============================
# LOGGING SETTINGS
# ==============================

LOG_CHANNEL_ID = 1398996215236001815

LOG_MESSAGES = True
LOG_MEMBER_EVENTS = True
LOG_MODERATION = True
LOG_ROLE_CHANGES = True
LOG_VOICE_CHANGES = True
LOG_NICKNAME_CHANGES = True


# ==============================
# EMBED SETTINGS
# ==============================

SUCCESS_COLOR = 0x57F287
ERROR_COLOR = 0xED4245
WARNING_COLOR = 0xFEE75C
INFO_COLOR = 0x5865F2

FOOTER_TEXT = "Moderation Bot"


# ==============================
# CONFIRMATION SYSTEM
# ==============================

CONFIRM_ACTIONS = True

CONFIRM_TIMEOUT = 60


# ==============================
# MODERATION SETTINGS
# ==============================

DM_PUNISHMENTS = True

STORE_CASES = True

AUTO_CASE_NUMBERS = True


# ==============================
# NICKNAME SYSTEM
# ==============================

NICKNAME_SEPARATOR = " | "

NICKNAME_SKIP_BOTS = True

NICKNAME_SEND_PROGRESS_DM = True

NICKNAME_PROGRESS_AMOUNT = 10


# ==============================
# AUTOMOD SETTINGS
# ==============================

AUTOMOD_ENABLED = True

ANTI_SPAM = True
ANTI_LINKS = True
ANTI_INVITES = True
ANTI_CAPS = True
ANTI_MENTION_SPAM = True
ANTI_DUPLICATES = True

BAD_WORD_FILTER = True


# ==============================
# TICKET SYSTEM
# ==============================

TICKETS_ENABLED = True

TICKET_CATEGORY_ID = None

TICKET_LOG_CHANNEL_ID = None


# ==============================
# VERIFICATION SYSTEM
# ==============================

VERIFICATION_ENABLED = False

VERIFICATION_CHANNEL_ID = None

VERIFIED_ROLE_ID = None


# ==============================
# GENERAL BOT SETTINGS
# ==============================

IGNORE_BOTS = True

OWNER_ONLY_MODE = True

DEBUG_MODE = False
