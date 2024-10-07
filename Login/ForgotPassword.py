from .utils import st, rx, requests, deconfig
from .Components import RX_Header, RX_BottomMenu, RX_Button

class RecoveryState(rx.State):
    email: str = ""
    response: dict = {}

    regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    @rx.background 
    async def recovery(self, data: dict) -> bool:
        """Call to recovery API to pass recovery"""        
        response = await requests.post(deconfig('FORGOT_PASSWORD_SENDER_EMAIL_API_URL'), json=data)
        if response == '200':
            return rx.redirect('recovery_succcefull')
        return rx.window_alert("Recovery password services are down, please try later")

    def pre_validate(self):
        """pre validate the provided email after send by api
        Args:
            ...
        Returns:
            rx.Component: if validation is successful
            bool: False if validation is not successful
        """
        if not self.email:
            return rx.window_alert("Email field are required!")
        return False
    
    def  validate(self) -> rx.Component:
        """Implement pre_validate y api_validate logic
        Args:
            ...
        Returns:
            rx.Component: if validation is successful
        """
        if not self.pre_validate():
            if self.api_validation({'email': RecoveryState.email}):
                return RecoveryState.recovery({'email': RecoveryState.email})
            return self.pre_validate()
        return True
        
    @rx.background   
    async def api_validation(self, data: dict) -> bool:
        """Validate the provided email and password
        Args:
            data (dict): A dictionary containing the following keys:
                - 'username': username to validate.
                - 'password': password to validate.

        Returns:
            bool: True if validation is successful, False otherwise.
        """
        response = await requests.post(deconfig('FORGOT_PASSWORD_API_URL'), json=data)
        if response == '200':
            return True
    
def RX_UserEntries(title: str, icon: str):
    return rx.vstack(
        rx.text(title, style = st.style_user_entries),
        rx.input(
            rx.input.slot(rx.icon(icon)),
            color = 'white', 
            width = '100%',
            type = 'text',
            on_change = RecoveryState.set_email,
            placeholder = 'user@example.com',
        ),
        width = '100%',
    )

def GUI_ForgotPassword():
    return rx.vstack(
        rx.hstack(
            rx.icon('key-round', style = st.icons),
            style = st.banner_header
        ),
        rx.vstack(
            RX_Header(text_header='Recovery your password'),
            RX_UserEntries('Email', 'user'),
            RX_BottomMenu(text='Back to Login', route='login'),
            rx.spacer(),
            RX_Button(text_button='Recovery your password', action = RecoveryState.validate),
            width = '100%',
            padding = '2em 2em 4em 2em'
        ),
        style = st.main_card
    )
    
@rx.page(route='/forgot_password', title='Forgot Password')
def Main() -> rx.Component:
    return rx.center(
            GUI_ForgotPassword(), 
            style = st.GUI_cards,
            )