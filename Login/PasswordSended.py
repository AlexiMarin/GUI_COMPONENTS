from .utils import st, rx, deconfig
from .Components import RX_BottomMenu

def GUI_Recovery():
    return rx.vstack(
        rx.hstack(
        ),
        rx.vstack(
            rx.hstack(rx.image(
                src = deconfig('IMAGE_PASSWORD__EMAIL__SENDED_') if deconfig('IMAGE_PASSWORD__EMAIL__SENDED_') else deconfig('IMAGE_PASSWORD__EMAIL__SENDED_PLACEHOLDER'),
                width = '3.2em',
                height = 'auto',
                border_radius = '25%',
                filter = 'invert(1)'
                ),
                rx.text('Email recovery succefull at your mail, please check it out!', )
            ),
            RX_BottomMenu('Back to Login', route = 'login'),
            width = '100%',
            height = '100%',
            padding = '2em 2em 4em 2em'
        ),
        style = st.main_card
    )

@rx.page(route='/recovery_succcefull', title='Recovery Succefull')
def Main() -> rx.Component:
    return rx.center(
        GUI_Recovery(), 
        style = st.GUI_cards,
        )