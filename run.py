from project import create_app  # Import the Flask app from views.py

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8888)  # Run the app