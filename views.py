import flet as ft
from datetime import datetime

# ===== ЦВЕТА =====
COLOR_BG_DARK = "#17212B"      # Основной фон
COLOR_SECONDARY = "#232E3C"    # Вторичный фон
COLOR_ACCENT = "#1F96C7"       # Акцент (голубой)
COLOR_TEXT_PRIMARY = "#FFFFFF" # Белый текст
COLOR_TEXT_SECONDARY = "#7A8288" # Серый текст
COLOR_BORDER = "#3D4D59"       # Граница

# ===== ВХОД =====
def login_view(go_to_reg, on_login_click):
    email = ft.TextField(
        label="Электронная почта",
        width=400,
        height=60,
        border_radius=10,
        bgcolor=COLOR_SECONDARY,
        border_color=COLOR_BORDER,
        text_size=15,
        color=COLOR_TEXT_PRIMARY,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, size=14),
        input_filter=ft.InputFilter(allow=True),
        filled=True
    )
    password = ft.TextField(
        label="Пароль",
        password=True,
        width=400,
        height=60,
        border_radius=10,
        bgcolor=COLOR_SECONDARY,
        border_color=COLOR_BORDER,
        text_size=15,
        color=COLOR_TEXT_PRIMARY,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, size=14),
        filled=True
    )
    
    return ft.Column([
        ft.Text("ChirpApp", size=50, weight="bold", color=COLOR_ACCENT),
        ft.Text("Secure Messaging", size=18, color=COLOR_TEXT_SECONDARY),
        ft.Divider(height=40, color="transparent"),
        ft.Text("Вход в аккаунт", size=20, color=COLOR_TEXT_PRIMARY, weight="w500"),
        ft.Divider(height=20, color="transparent"),
        email,
        ft.Divider(height=10, color="transparent"),
        password,
        ft.Divider(height=20, color="transparent"),
        ft.ElevatedButton(
            "🔓 Войти",
            on_click=lambda e: on_login_click(email.value, password.value),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=COLOR_ACCENT,
                color="white",
                padding=20
            ),
            width=400,
            height=60,
            text_style=ft.TextStyle(size=16, weight="bold")
        ),
        ft.Divider(height=20, color="transparent"),
        ft.Row([
            ft.Text("Нет аккаунта?", color=COLOR_TEXT_SECONDARY, size=14),
            ft.TextButton(
                "Создать аккаунт",
                on_click=go_to_reg,
                style=ft.ButtonStyle(color=COLOR_ACCENT),
                style_text=ft.TextStyle(size=14, weight="bold")
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    vertical_alignment=ft.MainAxisAlignment.CENTER,
    expand=True,
    spacing=0,
    bgcolor=COLOR_BG_DARK,
    padding=30
    )

# ===== РЕГИСТРАЦИЯ =====
def reg_view(go_to_login, on_reg_click):
    email = ft.TextField(
        label="Электронная почта",
        width=400,
        height=60,
        border_radius=10,
        bgcolor=COLOR_SECONDARY,
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        text_size=15,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, size=14),
        filled=True
    )
    password = ft.TextField(
        label="Пароль (минимум 6 символов)",
        password=True,
        width=400,
        height=60,
        border_radius=10,
        bgcolor=COLOR_SECONDARY,
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        text_size=15,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, size=14),
        filled=True
    )
    username = ft.TextField(
        label="Имя пользователя (3-15 символов)",
        width=400,
        height=60,
        border_radius=10,
        bgcolor=COLOR_SECONDARY,
        border_color=COLOR_BORDER,
        color=COLOR_TEXT_PRIMARY,
        text_size=15,
        label_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY, size=14),
        filled=True
    )
    
    return ft.Column([
        ft.Text("ChirpApp", size=50, weight="bold", color=COLOR_ACCENT),
        ft.Text("Создание аккаунта", size=18, color=COLOR_TEXT_SECONDARY),
        ft.Divider(height=40, color="transparent"),
        ft.Text("Регистрация", size=20, color=COLOR_TEXT_PRIMARY, weight="w500"),
        ft.Divider(height=20, color="transparent"),
        email,
        ft.Divider(height=10, color="transparent"),
        password,
        ft.Divider(height=10, color="transparent"),
        username,
        ft.Divider(height=20, color="transparent"),
        ft.ElevatedButton(
            "✅ Зарегистрироваться",
            on_click=lambda e: on_reg_click(email.value, password.value, username.value),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=COLOR_ACCENT,
                color="white",
                padding=20
            ),
            width=400,
            height=60,
            text_style=ft.TextStyle(size=16, weight="bold")
        ),
        ft.Divider(height=20, color="transparent"),
        ft.Row([
            ft.Text("Уже есть аккаунт?", color=COLOR_TEXT_SECONDARY, size=14),
            ft.TextButton(
                "Войти",
                on_click=go_to_login,
                style=ft.ButtonStyle(color=COLOR_ACCENT),
                style_text=ft.TextStyle(size=14, weight="bold")
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    vertical_alignment=ft.MainAxisAlignment.CENTER,
    expand=True,
    spacing=0,
    bgcolor=COLOR_BG_DARK,
    padding=30
    )

# ===== ЧАТЫ =====
def chats_view(users, on_chat_click, toggle_menu):
    search_field = ft.TextField(
        hint_text="Поиск чатов...",
        bgcolor=COLOR_SECONDARY,
        border=ft.InputBorder.OUTLINE,
        border_color=COLOR_BORDER,
        prefix_icon=ft.icons.SEARCH,
        expand=True,
        color=COLOR_TEXT_PRIMARY,
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY)
    )
    
    chat_list = []
    for username in users:
        chat_item = ft.Container(
            content=ft.Row([
                ft.CircleAvatar(
                    content=ft.Text(username[0].upper() if username else "?", color="white", size=16),
                    bgcolor=COLOR_ACCENT,
                    radius=25
                ),
                ft.Column([
                    ft.Text(username, size=15, color=COLOR_TEXT_PRIMARY, weight="bold"),
                    ft.Text("Привет!", size=12, color=COLOR_TEXT_SECONDARY)
                ], expand=True),
                ft.Text("14:54", size=12, color=COLOR_TEXT_SECONDARY)
            ], spacing=12),
            padding=12,
            on_click=lambda e, u=username: on_chat_click(u),
            bgcolor="transparent",
            border_radius=10,
            ink=True,
        )
        chat_list.append(chat_item)
    
    return ft.Container(
        content=ft.Column([
            # Заголовок
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        ft.icons.MENU,
                        on_click=toggle_menu,
                        icon_color=COLOR_TEXT_PRIMARY
                    ),
                    search_field,
                ], spacing=10),
                padding=10,
                bgcolor=COLOR_BG_DARK
            ),
            # Список чатов
            ft.ListView(
                chat_list if chat_list else [
                    ft.Container(
                        content=ft.Text(
                            "Нет чатов. Добавьте контакт!",
                            color=COLOR_TEXT_SECONDARY,
                            size=14
                        ),
                        padding=20,
                        alignment=ft.alignment.center
                    )
                ],
                expand=True,
                spacing=5,
                padding=10
            )
        ], expand=True, spacing=0),
        bgcolor=COLOR_BG_DARK,
        expand=True,
        width=350
    )

# ===== ОКНО ЧАТА =====
def chat_window(receiver_username, messages, on_send, is_online):
    msg_field = ft.TextField(
        hint_text="Введите сообщение...",
        expand=True,
        bgcolor=COLOR_SECONDARY,
        border_radius=20,
        border_color="transparent",
        color=COLOR_TEXT_PRIMARY,
        hint_style=ft.TextStyle(color=COLOR_TEXT_SECONDARY),
        min_lines=1,
        max_lines=4
    )
    
    message_list = []
    for msg in messages:
        sender, content, timestamp, is_read = msg
        is_own = False  # Эту логику нужно передать
        
        msg_bubble = ft.Container(
            content=ft.Text(
                content,
                color="white" if is_own else COLOR_TEXT_PRIMARY,
                size=14,
                selectable=True
            ),
            bgcolor=COLOR_ACCENT if is_own else COLOR_SECONDARY,
            border_radius=15,
            padding=ft.padding.symmetric(15, 10)
        )
        
        message_list.append(
            ft.Row(
                [msg_bubble],
                alignment=ft.MainAxisAlignment.END if is_own else ft.MainAxisAlignment.START,
                spacing=10
            )
        )
    
    def on_send_click(e):
        if msg_field.value.strip():
            on_send(receiver_username, msg_field.value)
            msg_field.value = ""
            msg_field.focus()
    
    return ft.Container(
        content=ft.Column([
            # Заголовок
            ft.Container(
                content=ft.Row([
                    ft.CircleAvatar(
                        content=ft.Text(receiver_username[0].upper(), color="white"),
                        bgcolor=COLOR_ACCENT,
                        radius=20
                    ),
                    ft.Column([
                        ft.Text(receiver_username, color=COLOR_TEXT_PRIMARY, weight="bold"),
                        ft.Text(
                            "🟢 В сети" if is_online else "⚫ Был недавно",
                            color=COLOR_TEXT_SECONDARY,
                            size=12
                        )
                    ], expand=True),
                    ft.IconButton(ft.icons.CALL, icon_color=COLOR_ACCENT),
                    ft.IconButton(ft.icons.VIDEO_CALL, icon_color=COLOR_ACCENT),
                    ft.IconButton(ft.icons.MORE_VERT, icon_color=COLOR_ACCENT)
                ], spacing=10),
                padding=15,
                bgcolor=COLOR_SECONDARY,
                border_bottom="1px solid " + COLOR_BORDER
            ),
            # Сообщения
            ft.ListView(
                message_list if message_list else [
                    ft.Container(
                        content=ft.Text(
                            "Начните разговор",
                            color=COLOR_TEXT_SECONDARY,
                            size=14
                        ),
                        padding=20,
                        alignment=ft.alignment.center
                    )
                ],
                expand=True,
                spacing=5,
                padding=15
            ),
            # Поле ввода
            ft.Container(
                content=ft.Row([
                    ft.IconButton(ft.icons.ADD, icon_color=COLOR_ACCENT),
                    msg_field,
                    ft.IconButton(
                        ft.icons.SEND,
                        on_click=on_send_click,
                        icon_color=COLOR_ACCENT
                    )
                ], spacing=10),
                padding=15,
                bgcolor=COLOR_BG_DARK
            )
        ], expand=True, spacing=0),
        bgcolor=COLOR_BG_DARK,
        expand=True
    )
