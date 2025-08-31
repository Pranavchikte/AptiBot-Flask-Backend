from flask import Flask, jsonify, request
from flask_cors import CORS
from .config import Config
from .ai_logic import solve_problem
from .file_processor import process_file
import uuid
import os
from werkzeug.utils import secure_filename

SESSIONS = {}
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH # Set the upload limit
    
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    CORS(app)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found: The requested URL was not found on the server."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error: Something went wrong on our end."}), 500
        
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method Not Allowed: The method is not allowed for the requested URL."}), 405

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({"error": "File Too Large: The file exceeds the 10MB upload limit."}), 413

    @app.route('/')
    def index():
        return jsonify({'message': "AptiBot server is up and running"})

    @app.route('/api/sessions', methods=['POST'])
    def create_session():
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = []
        return jsonify({"session_id": session_id})
    
    @app.route('/api/sessions/<session_id>/messages', methods=['POST'])
    def handle_chat_message(session_id):
        if session_id not in SESSIONS:
            return jsonify({"error": "Session not found"}), 404

        chat_history = SESSIONS[session_id]
        user_query = ""
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            extracted_text = process_file(filepath)
            
            if extracted_text.startswith("Error:"):
                return jsonify({"error": extracted_text}), 500
            
            user_query = extracted_text
            text_from_form = request.form.get('query', '')
            if text_from_form:
                 user_query = f"Context: {text_from_form}\n\nProblem from file '{filename}':\n{user_query}"
            
            SESSIONS[session_id].append({'role': 'user', 'parts': [user_query]})
        else:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "Request must contain a file upload or a JSON body with a 'query'"}), 400
            user_query = data.get('query')
            SESSIONS[session_id].append({'role': 'user', 'parts': [user_query]})
        
        solution = solve_problem(user_query, chat_history)
        SESSIONS[session_id].append({'role': 'model', 'parts': [solution]})
        
        return jsonify({"solution": solution})

    return app