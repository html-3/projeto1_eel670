from app import app

# forca o update com o código do master
# git push origin development:master -f
# lembrar de usar git pull regularmente

if __name__ == "__main__":
    
    app.run()