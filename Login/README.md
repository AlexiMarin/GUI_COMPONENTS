Configurar el .env e importar Main as:
----------------------
app = rx.App()
Main.add_pages()
app._compile()
----------------------

Esto crea las rutas:
----------------------
/login
/forgot_password
/singup
/recovery_succefull
----------------------