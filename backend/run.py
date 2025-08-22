#!/usr/bin/env python3
import os
from app import create_app, db, socketio
from dotenv import load_dotenv

load_dotenv()

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def reset_db():
    """Reset the database."""
    db.drop_all()
    db.create_all()
    print("Database reset!")

if __name__ == '__main__':
    # For development, run with Socket.IO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
