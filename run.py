from app import app
from app.dummy_data import create_dd

# forca o update com o código do master
# git push origin development:master -f
# lembrar de usar git pull regularmente

if __name__ == "__main__":
    create_dd()
    app.run()