from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

conversations = []

@app.route('/')
def index():
    return render_template('index.html', conversations=conversations)

@app.route('/process_form', methods=['POST'])
def process_form():
    user_input = request.form['user_input']
    response = process_user_input(user_input)
    conversations.append({'user': user_input, 'bot': response})
    return jsonify({'user_input': user_input, 'bot_response': response})

def process_user_input(user_input):
    # Add your processing logic here
    # You can call other functions, APIs, or perform any other tasks based on user_input
    # For demonstration purposes, simply echoing back the user input.
    return "You entered: " + user_input

# Serve static files (CSS in this case)
@app.route('chatbot.html')
def static_files(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True)
