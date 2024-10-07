from .utils import st, rx, deconfig

def RX_Header(text_header: str):
    return rx.hstack(
        rx.vstack(
            rx.image(
                src = deconfig('LOGO') if deconfig('LOGO') else deconfig('LOGO_PLACEHOLDER'),
                width = '2.5em',
                height = 'auto',
                border_radius = '25%'
            ),
            rx.heading(
                text_header,
                size = '7',
                as_ = 'h2',
                text_align = 'left',
                width = '100%',
            )
        )
    )

def RX_BottomMenu(text: str, route: str = '/login'):
    return rx.hstack(
        rx.spacer(),
        rx.link(
            text,
            style = st.bottom_button,
            on_click=lambda: rx.redirect(f'/{route}')
        ),
        width="100%",
    )
    
def RX_Button(text_button: str, action: any = None):
    return rx.button(
        rx.text(text_button, align='center', width = '100%'), 
        color_scheme= deconfig('BUTTON_COLOR'), 
        variant='outline', 
        size = '2', 
        width = '100%', 
        padding = '1em 01m',
        on_click = action
    )
    
def RX_UserEntries(title: str, placeholder: str, _icon: str = 'user', is_password: bool = False, action_password: any = None, action: any = None, _required: bool = False):
    icon = ''
    if not is_password:
        icon = _icon
    else:
        icon = 'key-round'
    return rx.vstack(
        rx.text(title, style = st.style_user_entries),
        rx.input(
            rx.input.slot(rx.icon(icon)),
            color = 'white', 
            width = '100%',
            type = 'text' if not is_password else 'password',
            on_change = action if not is_password else action_password,
            placeholder = placeholder,
            required= _required if _required else False
        ),
        width = '100%',
    )