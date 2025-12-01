"""
AI Chat controller for AI-powered meeting assistance
"""

from flask import jsonify, current_app, request
from ..models.ai_chat import AIChatSession, AIMessage
from ..middleware.auth_middleware import get_current_user_id

try:
    import google.generativeai as genai
    HAS_GENAI = True
    print("Google Generative AI loaded successfully")
except ImportError as e:
    print(f"Google Generative AI import failed: {e}")
    HAS_GENAI = False
    genai = None
except Exception as e:
    print(f"Google Generative AI initialization failed: {e}")
    HAS_GENAI = False
    genai = None

class AIController:
    """AI controller for AI chat functionality."""
    
    @staticmethod
    def chat():
        """Send a message to AI and get a response."""
        try:
            user_id = get_current_user_id()
            
            data = request.json
            message = data.get('message', '').strip()
            session_id = data.get('session_id', 'default')
            
            if not message:
                return jsonify({
                    'success': False,
                    'error': 'Message is required'
                }), 400
            
            # Check if Gemini API key is configured
            gemini_api_key = current_app.config.get('GEMINI_API_KEY')
            
            if gemini_api_key and HAS_GENAI:
                # Use actual Gemini API
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel(current_app.config.get('GEMINI_MODEL', 'gemini-1.5-flash'))
                    
                    # Create context-aware prompt for meeting management
                    system_prompt = """You are an AI assistant for a meeting management platform called FollowUp. 
                    Help users with meeting-related tasks, scheduling, follow-ups, and task management. 
                    Be concise, helpful, and professional."""
                    
                    full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
                    
                    response = model.generate_content(full_prompt)
                    ai_response = response.text
                    
                except Exception as e:
                    current_app.logger.error(f"Gemini API error: {e}")
                    ai_response = "I'm experiencing technical difficulties. Please try again later."
            else:
                # Use mock responses
                ai_response = AIController._get_mock_response(message)
            
            # Save chat to database
            session = AIChatSession.get_or_create_session(user_id, session_id)
            session.add_message(AIMessage('user', message))
            session.add_message(AIMessage('ai', ai_response))
            session.save(session_id, user_id)
            
            return jsonify({
                'success': True,
                'data': {
                    'message': ai_response,
                    'session_id': session_id
                }
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"AI chat error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to process AI request'
            }), 500
    
    @staticmethod
    def _get_mock_response(message):
        """Generate a mock AI response for testing."""
        message_lower = message.lower()
        
        if 'schedule' in message_lower or 'meeting' in message_lower:
            return "I can help you schedule meetings. Would you like to create a new meeting or view your upcoming schedule?"
        elif 'task' in message_lower:
            return "I can assist with task management. You can create tasks, set priorities, and track their progress."
        elif 'reminder' in message_lower or 'follow' in message_lower:
            return "I'll help you set up reminders and follow-ups. When would you like to be reminded?"
        elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your AI assistant for meeting management. How can I help you today?"
        else:
            return "I'm here to help with your meetings, tasks, and scheduling. What would you like to know?"
    
    @staticmethod
    def get_chat_history():
        """Get chat history for the current user."""
        try:
            user_id = get_current_user_id()
            session_id = request.args.get('session_id', 'default')
            
            session = AIChatSession.find_by_session_id(session_id, user_id)
            
            if not session:
                return jsonify({
                    'success': True,
                    'data': {
                        'messages': [],
                        'session_id': session_id
                    }
                }), 200
            
            session_dict = session.to_dict()
            
            return jsonify({
                'success': True,
                'data': {
                    'messages': session_dict.get('messages', []),
                    'session_id': session_dict.get('session_id')
                }
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get chat history error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch chat history'
            }), 500
