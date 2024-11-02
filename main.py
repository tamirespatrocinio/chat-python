import flet as ft


def main(page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    user_name = ""

    def send_websocket_message(msg):

        if ": " in msg:
            name, message = msg.split(": ", 1)
            is_user_message = name == box_name_popup.value

            chat.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(f"{name}: {message}",
                                    color=ft.colors.WHITE),
                            bgcolor=ft.colors.GREEN_400 if is_user_message else ft.colors.BLUE_400,
                            border_radius=100,
                            padding=10,
                            alignment=ft.alignment.center_left if not is_user_message else ft.alignment.center_right,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END if is_user_message else ft.MainAxisAlignment.START
                )
            )
            page.update()
        else:
            chat.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(msg, color=ft.colors.WHITE, size=12),
                            bgcolor=ft.colors.GREY_900,
                            border_radius=100,
                            padding=10,
                            alignment=ft.alignment.center,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
            page.update()

    page.pubsub.subscribe(send_websocket_message)

    def open_chat(e):
        popup.open = False
        page.remove(initial_container)
        page.add(chat_container)

        user_name = box_name_popup.value
        message = f"{user_name} entrou no chat"
        page.pubsub.send_all(message)
        page.update()

    title_popup = ft.Text("Boas-vindas ao PythonZap")
    box_name_popup = ft.TextField(label="Digite seu nome")
    button_popup = ft.ElevatedButton("Entrar no Chat", on_click=open_chat)

    popup = ft.AlertDialog(
        title=title_popup,
        content=box_name_popup,
        actions=[button_popup]
    )

    chat = ft.Column()

    def send_msg(e):
        message = f"{box_name_popup.value}: {box_on_msg.value}"
        page.pubsub.send_all(message)
        box_on_msg.value = ""
        page.update()

    box_on_msg = ft.TextField(
        label="Digite sua mensagem",
        on_submit=send_msg,
        width=485,
        border_radius=20,
        height=50,
        border="none",
        label_style=ft.TextStyle(color=ft.colors.WHITE, size=12),
        text_style=ft.TextStyle(color=ft.colors.WHITE)
    )

    button_send = ft.ElevatedButton(
        "Enviar", on_click=send_msg)
    row_send = ft.Row([box_on_msg, button_send])

    chat_container = ft.Container(
        alignment=ft.alignment.top_center,
        width=600,
        height=400,
        border_radius=10,
        padding=10,
        bgcolor=ft.colors.BLACK,
        content=ft.Column(
            [
                chat,
                row_send
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    def open_popup(e):
        page.overlay.append(popup)
        popup.open = True
        page.update()

    initial_container = ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK,
        width=600,
        height=400,
        border_radius=10,
        content=ft.Column(
            [
                ft.Text(
                    "PythonZap", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Iniciar Chat", on_click=open_popup)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    page.add(initial_container)


ft.app(main, view=ft.AppView.WEB_BROWSER)
