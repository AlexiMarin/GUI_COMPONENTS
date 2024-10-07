from .utils import deconfig

def ExternalComponentsValidation(component: str):
    if str(deconfig(component)) == 'True':
        return True
    return False   