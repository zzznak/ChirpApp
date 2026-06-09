import asyncio
import websockets
import json
import flet as ft
import re
from database import register_user, check_login, get_all_users, get_chat_history, get_user_status
from views import login_view, reg_view, chats_view, chat_window, COLOR_BG_DARK, COLOR_SECONDARY, COLOR_ACCENT, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY
from security import CryptoManager
from datetime import datetime

# ===== ЦВЕТА =====
COLOR_BG_DARK = "#17212B"
COLOR_SECONDARY = "#232E3C"
COLOR_ACCENT = "#1F96C7"
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_SECONDARY = "#7A8288"

# ===== ВАЛИДАЦИЯ EMAIL =====
def validate_email(email):
    """Проверяет корректность email адреса"""
    # Более строгая проверка email
    email_regex = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$'
    
    if not email or len(email) > 254:
        return False, "Email должен содержать от 1 до 254 символов"
    
    if not re.match(email_regex, email):
        return False, "Неверный формат email (пример: user@example.com)"
    
    # Проверка на запрещенные символы
    if '..' in email:
        return False, "Email не может содержать две точки подряд"
    
    if email.endswith('.'):
        return False, "Email не может заканчиваться на точку"
    
    # Проверка на популярные доменные имена
    valid_domains = [
        'gmail.com', 'yandex.ru', 'mail.ru', 'outlook.com', 'yahoo.com',
        'hotmail.com', 'rambler.ru', 'bk.ru', 'inbox.ru', 'list.ru',
        'mail.ua', 'ukr.net', 'i.ua'
    ]
    
    domain = email.split('@')[1].lower()
    # Если домен не в списке популярных, то можно использовать, но это рискованнее
    
    return True, "OK"

def validate_password(password):
    """Проверяет надежность пароля"""
    if not password:
        return False, "Пароль не может быть пустым"
    
    if len(password) < 6:
        return False, "Пароль должен содержать минимум 6 символов"
    
    if len(password) > 128:
        return False, "Пароль слишком длинный (макс. 128 символов)"
    
    return True, "OK"

def validate_username(username):
    """Проверяет корректность юзернейма"""
    if not username:
        return False, "Юзернейм не может быть пустым"
    
    if len(username) < 3:
        return False, "Юзернейм должен содержать минимум 3 символа"
    
    if len(username) > 15:
        return False, "Юзернейм может содержать максимум 15 символов"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Юзернейм может содержать только латиницу, цифры и подчеркивание"
    
    if username[0].isdigit():
        return False, "Юзернейм не может начинаться с цифры"
    
    return True, "OK"

async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLOR_BG_DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 700
    page.window_min_width = 900
    page.window_min_height = 600
    page.title = "ChirpApp - Secure Messenger"
    
    # Инициализация безопасности
    crypto = CryptoManager()
    current_user_email = None
    current_username = None
    
    # Глобальное соединение с сервером
    global_websocket = None
    
    # Контейнер для основного контента
    content_area = ft.Container(expand=True)
    
    # Хранилище сообщений чатов
    chat_messages = {}  # {username: [messages]}
    current_chat = None  # Текущий открытый чат
    
    async def listen_to_server(username):
        nonlocal global_websocket
        uri = f"ws://localhost:8000/ws/{username}"
        try:
            async with websockets.connect(uri) as websocket:
                global_websocket = websocket
                print(f"✅ Подключено к серверу")
                while True:
                    try:
                        msg = await websocket.recv()
                        data = json.loads(msg)
                        msg_type = data.get('type', 'message')
                        
                        if msg_type == 'message':
                            from_user = data['from']
                            content = data['content']
                            timestamp = data.get('timestamp', str(datetime.now()))
                            
                            # Расшифруем
                            try:
                                decrypted = crypto.decrypt(content)
                            except:
                                decrypted = content
                            
                            print(f"📨 Сообщение от {from_user}: {decrypted}")
                            
                            # Сохраняем в памяти
                            if from_user not in chat_messages:
                                chat_messages[from_user] = []
                            chat_messages[from_user].append((from_user, decrypted, timestamp, False))
                            
                            # Если это текущий чат, обновляем
                            if current_chat == from_user:
                                page.run_task(refresh_current_chat)
                                
                        elif msg_type == 'typing':
                            print(f"⌨️ {data['from']} печатает...")
                            
                    except Exception as e:
                        print(f"Ошибка получения сообщения: {e}")
                        break
        except Exception as e:
            print(f"❌ Сервер недоступен: {e}")
            show_error("Ошибка соединения с сервером")
    
    async def send_message(target_user, text):
        if global_websocket:
            try:
                # Шифруем перед отправкой
                encrypted_text = crypto.encrypt(text)
                # Упаковываем в JSON
                payload = json.dumps({
                    "target": target_user,
                    "content": encrypted_text,
                    "type": "message"
                })
                # Шлем на сервер
                await global_websocket.send(payload)
                print(f"📤 Отправлено пользователю {target_user}")
                
                # Сохраняем себе в историю
                if target_user not in chat_messages:
                    chat_messages[target_user] = []
                chat_messages[target_user].append((current_username, text, str(datetime.now()), True))
                
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                show_error("Ошибка при отправке сообщения")
        else:
            show_error("Нет соединения с сервером")
    
    async def refresh_current_chat():
        if current_chat:
            # Обновляем UI чата
            open_chat(current_chat)
    
    def show_error(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor="#FF4444",
            duration=3000
        )
        page.snack_bar.open = True
        page.update()
    
    def show_success(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=COLOR_ACCENT,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()
    
    def reg_handler(email, password, username):
        # Проверка email
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            show_error(f"Email: {error_msg}")
            return
        
        # Проверка пароля
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            show_error(f"Пароль: {error_msg}")
            return
        
        # Проверка юзернейма
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            show_error(f"Юзернейм: {error_msg}")
            return
        
        if register_user(email, password, username):
            show_success("✅ Регистрация успешна! Теперь войдите.")
            go_to_login(None)
        else:
            show_error("❌ Этот email или юзернейм уже заняты.")
    
    def login_handler(email, password):
        nonlocal current_user_email, current_username
        
        # Проверка email
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            show_error(f"Email: {error_msg}")
            return
        
        # Проверка пароля
        if not password:
            show_error("Пароль не может быть пустым")
            return
        
        user_name = check_login(email, password)
        
        if user_name:
            current_user_email = email
            current_username = user_name
            page.run_task(listen_to_server, user_name)
            show_success(f"✅ Добро пожаловать, {user_name}!")
            go_to_chats(None)
        else:
            show_error("❌ Неверный email или пароль")
    
    def open_chat(receiver_username):
        nonlocal current_chat
        current_chat = receiver_username
        
        # Загружаем историю
        history = get_chat_history(current_username, receiver_username)
        if receiver_username not in chat_messages:
            chat_messages[receiver_username] = history
        
        messages = chat_messages.get(receiver_username, [])
        is_online = get_user_status(receiver_username)
        
        # Функция отправки
        def on_send(target, text):
            page.run_task(send_message, target, text)
            page.update()
        
        # Создаем окно чата
        chat_view = chat_window(receiver_username, messages, on_send, is_online)
        
        # Создаем контейнер с левой панелью и чатом
        users = get_all_users(current_user_email) or []
        chats_panel = chats_view(users, open_chat, toggle_menu)
        
        content_area.content = ft.Row([
            chats_panel,
            ft.VerticalDivider(width=1, color=COLOR_SECONDARY),
            chat_view
        ], expand=True, spacing=0)
        page.update()
    
    def go_to_chats(e):
        users = get_all_users(current_user_email) or []
        chats_panel = chats_view(users, open_chat, toggle_menu)
        content_area.content = chats_panel
        page.update()
    
    def toggle_menu(e=None):
        # В полной версии здесь будет боковое меню
        show_error("📋 Меню: Профиль, Настройки, О программе")
    
    def go_to_reg(e):
        content_area.content = reg_view(go_to_login, reg_handler)
        page.update()
    
    def go_to_login(e):
        content_area.content = login_view(go_to_reg, login_handler)
        page.update()
    
    # Начальный экран входа
    content_area.content = login_view(go_to_reg, login_handler)
    
    # Сборка интерфейса
    page.add(
        ft.Container(
            content=content_area,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
