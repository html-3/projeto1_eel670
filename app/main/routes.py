from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)

@main.route("/", methods = ["GET"])
@main.route("/home")
def home():
    print(request.path)
    return render_template('home.html', title='Home')
