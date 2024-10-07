from .tools import ExternalComponentsValidation
import reflex as rx
from . import Login
from . import ForgotPassword
from . import SingUp
from . import PasswordSended

def add_pages():
    rx.App().add_page(Login.Main)
    if ExternalComponentsValidation('PASSWORD_RECOVERY'):
        rx.App().add_page(ForgotPassword.Main)
        rx.App().add_page(PasswordSended.Main)
    if ExternalComponentsValidation('SING_UP'):
        print('yes')
        rx.App().add_page(SingUp.Main)