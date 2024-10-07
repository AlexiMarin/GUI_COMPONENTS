from .utils import st, rx, requests, re, deconfig
from .Components import RX_Header, RX_BottomMenu, RX_Button, RX_UserEntries
from .tools import ExternalComponentsValidation

from . import ForgotPassword
from . import SingUp

class ScreenState(rx.State):
    current_screen: str = 'login'
    
    def SwitchScreens(self, screen: str):
        self.current_screen = screen
        
class LoginState(rx.State):   
    email: str = ""
    password: str = ""
    response: dict = {}

    regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    regex_password = r'^(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$'

    def pre_validate(self):
        """pre validate the provided email and password after send by api
        Args:
            ...
        Returns:
            rx.Component: if validation is successful
            bool: False if validation is not successful
        """
        if not self.email or not self.password:
            return rx.window_alert("Both fields are required!")
        
        if not re.match(self.regex_email, self.email):
            return rx.window_alert("Invalid email format!")

        if not re.match(self.regex_password, self.password):
            return rx.window_alert(
                "Password must be at least 8 characters, with one uppercase letter, one number, and one special character!"
            )
        return False
    
    def  validate(self) -> rx.Component:
        """Implement pre_validate y api_validate logic
        Args:
            ...
        Returns:
            rx.Component: if validation is successful
        """
        if not self.pre_validate():
            if self.api_validation({'email': LoginState.email,'password': LoginState.password}):
                return rx.window_alert("Si") #Enrutar
        else: 
            return self.pre_validate()
        
    @rx.background   
    async def api_validation(self, data: dict) -> bool:
        """Validate the provided email and password
        Args:
            data (dict): A dictionary containing the following keys:
                - 'email': email to validate.
                - 'password': password to validate.

        Returns:
            bool: True if validation is successful, False otherwise.
        """
        response = await requests.post(deconfig('LOGIN_API_URL'), json=data)
        if response == '200':
            return True
    
def RX_ThirtPartyLogin(title: str):
    return rx.button(
                rx.icon(tag=title),
                f'Sign in with {title}',
                variant = 'outline',
                size = '3',
                width = '100%'
            ),

def UI_ThirtPartyLogin():
    third_party_logins = [
        RX_ThirtPartyLogin(partner) for partner in eval(deconfig('EXTERNAL_LOGIN_PARTNERS'))
    ] 
    return rx.hstack(
        rx.vstack(
            rx.spacer(),
            rx.hstack(
                rx.divider(margin = '2', size = '4'),
                rx.text(
                    'Or continue with',
                    white_space="nowrap",
                    weight="medium",
                ),
                rx.divider(margin = "2", size = '4'),
            rx.spacer(),
                align='center',
                width = '100%'
            ),
            rx.spacer(),
            *third_party_logins,
            align="center",
            width="100%",
        ),
        align="center",
        spacing = '6',
        width = '100%'
    )

def RX_SingUp_Button():
    return rx.button(
        rx.text('Sign Up', align='center', width='100%'), 
        color_scheme='pink', 
        variant='outline', 
        size='2', 
        width='45%', 
        padding='1em 1em',
        margin='0 auto',
        on_click = lambda: rx.redirect('/singup')
    )

def UI_SingUp():
    return rx.hstack(
        rx.vstack(
            rx.spacer(),
            rx.hstack(
                rx.divider(margin='2', size='4'),
                rx.text(
                    'If you have no an account',
                    white_space="nowrap",
                    weight="medium",
                ),
                rx.spacer(),
                align='center',
                width='100%'
            ),
            rx.spacer(),
            rx.hstack(
                rx.spacer(),
                RX_SingUp_Button(),
                width='100%'
            ),
            align="center",
            width="100%",
        ),
        align="center",
        spacing='6',
        width='100%'
    )  

def GUI_Login():
    children = [
        RX_Header(text_header='Login'),
        rx.spacer(),
        RX_UserEntries(
            'Email', 
            action=LoginState.set_email, 
            placeholder='user@example.com'
        ),
        RX_UserEntries(
            'Password', 
            is_password=True,
            placeholder='Password',
            action_password=LoginState.set_password
        ),
        rx.spacer(),
        RX_Button(
            text_button='Login', 
            action=LoginState.validate
        ),
        rx.spacer(),
        rx.spacer(),
    ]
        
    if ExternalComponentsValidation('PASSWORD_RECOVERY'):
        children.insert(5, RX_BottomMenu('Forgot password?', 'forgot_password'))
    
    if ExternalComponentsValidation('EXTERNAL_LOGIN'):
        children.insert(-2, UI_ThirtPartyLogin())
        
    if ExternalComponentsValidation('SING_UP'):
        children.insert(-1, UI_SingUp())

    return rx.vstack(
        rx.hstack(
            rx.icon('lock', style=st.icons),
            style=st.banner_header
        ),
        rx.vstack(*children, width='100%', padding='2em 2em 4em 2em'),
        style=st.main_card
    )

    
@rx.page(route='/login', title='Login')
def Main() -> rx.Component:
    return rx.center(
        GUI_Login(),
        style = st.GUI_cards,
    )