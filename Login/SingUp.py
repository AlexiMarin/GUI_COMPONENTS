from .utils import st, rx, requests, re, deconfig
from .Components import RX_BottomMenu, RX_Button, RX_Header, RX_UserEntries


class ScreenState(rx.State):
    current_screen: str = 'singup'
    
    def SwitchScreens(self, screen: str):
        self.current_screen = screen
        
class SingUpState(rx.State):  
    name: str = ''
    last_name: str = '' 
    email: str = ""
    password: str = ""
    re_password: str = ''
    response: dict = {}

    regex_names = r'^[^\s]+$'
    regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    regex_password = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'


    def pre_validate(self):
        """
        pre validate the provided email, name, last name and password after send by api
        Args:
            ...
        Returns:
            rx.Component: if validation is successful
            bool: False if validation is not successful
        """
        print(self.email, self.name, self.last_name, self.password, self.re_password)
        if not self.email or not self.password or not self.last_name or not self.re_password or not self.name:
            return rx.window_alert("All fields are required!")
        
        if not re.match(self.regex_email, self.email):
            return rx.window_alert("Invalid email format!")
        
        if not re.match(self.regex_names, self.name):
            return rx.window_alert("Invalid Name format!")
        
        if not re.match(self.regex_names, self.last_name):
            return rx.window_alert("Invalid Last Name format!")
        
        if not re.match(self.regex_password, self.re_password):
            return rx.window_alert(
                "Password Confirmation must be at least 8 characters, with one uppercase letter, one number, and one special character!"
            )
        if not re.match(self.regex_password, self.password):
            return rx.window_alert(
                "Password must be at least 8 characters, with one uppercase letter, one number, and one special character!"
            )
        if self.password != self.re_password:
            return rx.window_alert("Passwords do not match!")
        
        return False
    
    def  validate(self) -> rx.Component:
        """
        Implement pre_validate y api_validate logic
        Args:
            ...
        Returns:
            rx.Component: if validation is successful
        """
        if not self.pre_validate():
            if self.api_validation({'email': SingUpState.email,
                                    'name': SingUpState.name,
                                    'last_name': SingUpState.last_name,
                                    'password': SingUpState.password,
                                    're_password': SingUpState.re_password,
                                    }):
                return rx.redirect('/login')
        else: 
            return self.pre_validate()
        
    @rx.background   
    async def api_validation(self, data: dict) -> bool:
        """
        Validate the provided email and password
        Args:
            data (dict): A dictionary containing the following keys:
                - 'email': email to validate.
                - 'password': password to validate.

        Returns:
            bool: True if validation is successful, False otherwise.
        """
        response = await requests.post(deconfig('SINGUP_API_URL'), json=data)
        if response == '200':
            return True
        return rx.window_alert("Sing up services are down, please try later")


def GUI_SingUp():
    return rx.vstack(
        rx.hstack(
            rx.icon('lock', style = st.icons),
            style = st.banner_header
        ),
        rx.vstack(
            RX_Header('Sing Up'),
            RX_UserEntries(title='Name', placeholder='Write your single name', action=SingUpState.set_name),
            RX_UserEntries(title='Last Name', placeholder='Write your last name', action=SingUpState.set_last_name),
            RX_UserEntries(title='Email', placeholder='Write your email', _icon = 'mail', action=SingUpState.set_email),
            RX_UserEntries(title='Password', placeholder='Write your password', is_password=True, action_password=SingUpState.set_password),
            RX_UserEntries(title='Password Confirmation', placeholder='Rewrite your password', is_password=True, action_password=SingUpState.set_re_password),
            RX_BottomMenu('Back to Login', route = 'login'),
            RX_Button(text_button='Sing Up', action=SingUpState.validate),
            width = '100%',
            height = '100%',
            padding = '2em 2em 4em 2em'
        ),
        style = st.main_card
    )

@rx.page(route='/singup', title='Sing Up')
def Main() -> rx.Component:
    return rx.center(
        GUI_SingUp(), 
        style = st.GUI_cards,
        )