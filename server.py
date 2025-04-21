# from flask import Flask
# from app.routes import main

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(main)
#     return app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)


from app.routes import main
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecurekey'
    app.register_blueprint(main)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
