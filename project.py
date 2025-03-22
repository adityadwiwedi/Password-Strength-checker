import flet as ft
import re
import random
import string

class AppWindow(ft.UserControl):
    def __init__(self):
        super().__init__()

        # Password field state
        self.is_password_visible = False  

        # Password input field
        self.password_field = ft.TextField(
            hint_text="Start typing a password...",
            text_size=14,
            bgcolor="transparent",
            border_color="transparent",
            color="white",
            password=True,
            on_change=self.check_password_strength,
            expand=True  
        )

        # Strength Bars
        self.length_bar = ft.ProgressBar(width=200, value=0, color="green")
        self.char_bar = ft.ProgressBar(width=200, value=0, color="green")
        self.repeat_bar = ft.ProgressBar(width=200, value=0, color="green")
        self.sequence_bar = ft.ProgressBar(width=200, value=0, color="red")

        # Strength Indicator Text
        self.strength_text = ft.Text("", size=12, color="white")

        # Icons
        self.length_icon = ft.Icon(ft.icons.CHECK, color="green", visible=False)
        self.char_icon = ft.Icon(ft.icons.CHECK, color="green", visible=False)
        self.repeat_icon = ft.Icon(ft.icons.CHECK, color="green", visible=False)
        self.sequence_icon = ft.Icon(ft.icons.CLOSE, color="red", visible=False)

        # Light/Dark Mode Toggle
        self.is_dark_mode = True
        self.theme_toggle = ft.IconButton(
            icon=ft.icons.DARK_MODE, icon_color="white", on_click=self.toggle_theme
        )

    def check_password_strength(self, e):
        password = self.password_field.value.strip()

        # Initialize score
        score = 0

        # Length Check
        if len(password) >= 12:
            self.length_bar.value, self.length_icon.visible = 1, True
            score += 1
        else:
            self.length_bar.value, self.length_icon.visible = 0.2, False

        # Character Check
        if (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and 
            re.search(r'\d', password) and re.search(r'[!@#$%^&*()_+]', password)):
            self.char_bar.value, self.char_icon.visible = 1, True
            score += 1
        else:
            self.char_bar.value, self.char_icon.visible = 0.2, False

        # Repeat Check
        if len(set(password)) > len(password) * 0.7:
            self.repeat_bar.value, self.repeat_icon.visible = 1, True
            score += 1
        else:
            self.repeat_bar.value, self.repeat_icon.visible = 0.2, False

        # Sequential Check
        if re.search(r'(123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij)', password, re.I):
            self.sequence_bar.value, self.sequence_icon.visible = 0.2, True
        else:
            self.sequence_bar.value, self.sequence_icon.visible = 1, False
            score += 1

        # Update Strength Indicator
        strength_levels = ["Weak 🔴", "Medium 🟡", "Strong 🟢"]
        self.strength_text.value = strength_levels[min(score, 2)]

        # Update UI
        self.update()

    def toggle_password_visibility(self, e):
        self.is_password_visible = not self.is_password_visible
        self.password_field.password = not self.is_password_visible
        e.control.icon = ft.icons.VISIBILITY if self.is_password_visible else ft.icons.VISIBILITY_OFF
        self.update()

    def copy_password(self, e):
        if self.password_field.value:
            e.page.set_clipboard(self.password_field.value)
            e.page.snack_bar = ft.SnackBar(ft.Text("Password copied!"), bgcolor="green")
            e.page.snack_bar.open = True
            e.page.update()

    def generate_password(self, e):
        generated_password = ''.join(random.choices(
            string.ascii_letters + string.digits + "!@#$%^&*()", k=14))
        self.password_field.value = generated_password
        self.check_password_strength(None)  # Recalculate strength
        self.update()

    def toggle_theme(self, e):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_toggle.icon = ft.icons.LIGHT_MODE if self.is_dark_mode else ft.icons.DARK_MODE
        self.update()

    def password_strength_display(self):
        return ft.Container(
            width=350,
            height=420,
            bgcolor="#1f262f",
            border_radius=10,
            padding=10,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Row([ft.Text("Password Strength Check", size=21, weight="bold", color="white"),
                            self.theme_toggle]),

                    ft.Text("Type in a password and see how strong it is!", size=12, color="white54"),
                    self.strength_text,

                    # Length Check
                    ft.Row([ft.Text("1. Length Check", color="white"), self.length_icon]),
                    self.length_bar,

                    # Character Check
                    ft.Row([ft.Text("2. Character Check", color="white"), self.char_icon]),
                    self.char_bar,

                    # Repeat Check
                    ft.Row([ft.Text("3. Repeat Check", color="white"), self.repeat_icon]),
                    self.repeat_bar,

                    # Sequential Check
                    ft.Row([ft.Text("4. Sequential Check", color="white"), self.sequence_icon]),
                    self.sequence_bar,
                ],
            ),
        )

    def password_input_display(self):
        return ft.Container(
            width=320,
            height=55,
            border_radius=12,
            bgcolor="#2a2f38",
            padding=ft.padding.only(left=15, right=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(expand=True, controls=[
                        ft.Icon(ft.icons.LOCK_OUTLINE_ROUNDED, size=18, opacity=0.85, color="white"),
                        self.password_field,
                    ]),
                    ft.Row(controls=[
                        ft.IconButton(
                            icon=ft.icons.VISIBILITY_OFF, icon_size=18, icon_color="white",
                            on_click=self.toggle_password_visibility
                        ),
                        ft.IconButton(
                            icon=ft.icons.CONTENT_COPY, icon_size=18, icon_color="white",
                            on_click=self.copy_password
                        )
                    ])
                ]
            )
        )

    def action_buttons(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton(text="Generate Strong Password", on_click=self.generate_password),
            ]
        )

    def build(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    self.password_strength_display(),
                    self.password_input_display(),
                    self.action_buttons()
                ],
            ),
        )

def main(page: ft.Page):
    page.title = "Password Strength Checker"
    page.bgcolor = "#0f1216"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(AppWindow())

ft.app(target=main)
