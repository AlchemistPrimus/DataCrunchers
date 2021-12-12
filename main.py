"""This is the main file that starts the application.
Here we call the app factory function to start our application."""
from app import create_app


if __name__=="__main__":
    create_app()