import os
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

# ============ КОНФИГУРАЦИЯ ============
BOT_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
ADMIN_IDS = [123456789]  # Ваш Telegram ID

# Настройки
DAILY_PERCENT = 0.01  # 1% в сутки
MIN_WITHDRAW = 15     # Минимальный вывод
WITHDRAW_COOLDOWN = 3 # Дней между выводами

# ============ БАЗА ДАННЫХ (в памяти) ============
users_db: Dict[int, Dict] = {}
tasks_db: List[Dict] = []
transactions_db: List[Dict] = []

# Инициализация тестовых данных
def init_test_data():
    """Создаем тестовые задания"""
    global tasks_db
    tasks_db = [
        {
            'id': 1,
            'type': 'subscribe',
            'title': 'Подписаться на канал',
            'description': 'Подпишитесь на наш канал',
            'reward': 0.5,
            'link': 'https://t.me/your_channel'
        },
        {
            'id': 2,
            'type': 'subscribe',
            'title': 'Вступить в группу',
            'description': 'Вступите в нашу группу',
            'reward': 0.5,
            'link': 'https://t.me/your_group'
        },
        {
            'id': 3,
            'type': 'social',
            'title': 'Сделать репост',
            'description': 'Сделайте репост записи',
            'reward': 1.0
        },
        {
            'id': 4,
            'type': 'social',
            'title': 'Оставить комментарий',
            'description': 'Оставьте комментарий под постом',
            'reward': 0.5
        },
        {
            'id': 5,
            'type': 'social',
            'title': 'Поставить лайк',
            'description': 'Поставьте лайк посту',
            'reward': 0.3
        }
    ]

# ============ ФУНКЦИИ РАБОТЫ С ПОЛЬЗОВАТЕЛЯМИ ============
def get_or_create_user(user_id: int, username: str = "") -> Dict:
    """Получить или создать пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {
            'id': user_id,
            'username': username,
            'balance': 0.0,
            'total_earned': 0.0,
            'deposited': 0.0,
            'withdrawn': 0.0,
            'referrals': 0,
            'referral_from': None,
            'tasks_completed': 0,
            'completed_task_ids': [],
            'daily_bonus_day': 1,
            'last_bonus_date': None,
            'last_withdraw_date': None,
            'created_at': datetime.now(),
            'joined_channels': False
        }
    return users_db[user_id]

def calculate_daily_income(user_id: int) -> float:
    """Рассчитать дневной доход (1% от баланса)"""
    user = users_db.get(user_id)
    if user:
        return user['balance'] * DAILY_PERCENT
    return 0.0

def can_withdraw(user_id: int) -> tuple:
    """Проверить, может ли пользователь выводить"""
    user = users_db.get(user_id)
    if not user:
        return False, "Пользователь не найден"
    
    # Проверка условий
    has_tasks = user['tasks_completed'] >= 10
    has_deposit = user['deposited'] >= 50
    has_balance = user['balance'] >= MIN_WITHDRAW
    
    if not (has_tasks or has_deposit):
        return False, "Выполните 10 заданий ИЛИ пополните на 50⭐"
    
    if not has_balance:
        return False, f"Минимум для вывода: {MIN_WITHDRAW}⭐"
    
    # Проверка кулдауна
    if user['last_withdraw_date']:
        days_passed = (datetime.now() - user['last_withdraw_date']).days
        if days_passed < WITHDRAW_COOLDOWN:
            days_left = WITHDRAW_COOLDOWN - days_passed
            return False, f"Вывод раз в {WITHDRAW_COOLDOWN} дня. Ждите: {days_left} дн."
    
    return True, "Можно выводить"

# ============ ФУНКЦИИ БОНУСОВ ============
def get_daily_bonus_amount(day: int) -> float:
    """Получить сумму бонуса для дня"""
    return 0.10 + (day - 1) * 0.025

def can_get_bonus(user_id: int) -> tuple:
    """Проверить, может ли получить бонус"""
    user = users_db.get(user_id)
    if not user:
        return False, "Пользователь не найден"
    
    today = datetime.now().date()
    last_bonus = user['last_bonus_date']
    
    if last_bonus and last_bonus.date() == today:
        return False, "Вы уже получали бонус сегодня"
    
    return True, "Можно получить бонус"

# ============ ФУНКЦИИ ЗАДАНИЙ ============
def complete_task(user_id: int, task_id: int) -> tuple:
    """Выполнить задание"""
    user = users_db.get(user_id)
    task = next((t for t in tasks_db if t['id'] == task_id), None)
    
    if not user:
        return False, "Пользователь не найден"
    if not task:
        return False, "Задание не найдено"
    if task_id in user['completed_task_ids']:
        return False, "Задание уже выполнено"
    
    # Начисляем награду
    reward = task['reward']
    user['balance'] += reward
    user['total_earned'] += reward
    user['tasks_completed'] += 1
    user['completed_task_ids'].append(task_id)
    
    return True, f"Задание выполнено! +{reward}⭐"

# ============ ПРИМЕР ИСПОЛЬЗОВАНИЯ ============
if __name__ == "__main__":
    # Инициализируем тестовые данные
    init_test_data()
    
    # Пример работы
    user_id = 123456
    user = get_or_create_user(user_id, "test_user")
    
    print(f"Создан пользователь: {user['username']}")
    print(f"Баланс: {user['balance']}⭐")
    print(f"Дневной доход: {calculate_daily_income(user_id)}⭐")
    
    # Пробуем выполнить задание
    success, message = complete_task(user_id, 1)
    print(f"Задание 1: {message}")
    print(f"Новый баланс: {user['balance']}⭐")
    
    # Проверяем вывод
    can_with, reason = can_withdraw(user_id)
    print(f"Может выводить: {can_with} ({reason})")
    
    # Проверяем бонус
    can_bonus, bonus_reason = can_get_bonus(user_id)
    print(f"Может получить бонус: {can_bonus} ({bonus_reason})")
    
    if can_bonus:
        bonus_amount = get_daily_bonus_amount(user['daily_bonus_day'])
        print(f"Бонус за день {user['daily_bonus_day']}: {bonus_amount}⭐")
