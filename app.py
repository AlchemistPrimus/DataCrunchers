"""This is the factory function that starts the application when called by the main file."""
from flask import Flask
from endpoints import routes

def create_app(config="settings"):
    app=Flask(__name__)
    
    
    app.register_blueprint(routes)
    
    return app.run(debug=True)