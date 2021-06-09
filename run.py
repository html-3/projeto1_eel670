from app import app
#from app.dummy_data import create_dd

# forca o update com o código do master
# git push origin development:master -f

if __name__ == "__main__":
    #create_dd()
    app.run()

# sqlalchemy.exc.IntegrityError
# sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: usuario.email
# [SQL: INSERT INTO usuario (nome_usuario, senha, email, confirmado, admin) VALUES (?, ?, ?, ?, ?)]
# [parameters: ('HENRIQUE MARQUES LOZANO', '$2b$12$qrYtpZus9tu3K0CyG/UrzeJZihC.WcSTERVrDFSORr4OO9498FtSG', 'henriquelozano2001@gmail.com', 0, 0)]
# (Background on this error at: http://sqlalche.me/e/13/gkpj)