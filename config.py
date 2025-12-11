import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ID администраторов
ADMIN_IDS = [123456789]  # Ваш ID

# Настройки системы
DAILY_PERCENT = 0.01  # 1% в сутки
MIN_WITHDRAW = 15     # Минимальный вывод
WITHDRAW_COOLDOWN = 3 # Дней между выводами
MIN_DEPOSIT = 10      # Минимальное пополнение

# Настройки заданий
TASK_REWARDS = {
    'subscribe': 0.5,  # Подписка
    'social': 1.0,     # Социальные действия
    'game': 2.0        # Игровые задания
}

# Настройки бонусов
BONUS_START = 0.10     # Начальный бонус
BONUS_INCREMENT = 0.025 # Увеличение в день
BONUS_MAX_DAY = 30     # Максимальный день

# Обязательные каналы (получить ID через @username_to_id_bot)
REQUIRED_CHANNELS = [
    -1001234567890,  # ID вашего канала
    -1009876543210   # ID вашей группы
]

# Настройки рефералов
REFERRAL_REWARD = 1.0  # Награда за реферала
