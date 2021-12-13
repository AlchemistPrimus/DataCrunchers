"""This is the factory function that starts the application when called by the main file."""
from flask import Flask
from endpoints import routes

app=Flask(__name__)
    
    
app.register_blueprint(routes)
    
   

if __name__=="__main__":
    app.run()
