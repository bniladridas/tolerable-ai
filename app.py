"""
Tolerable AI - A web application that uses the Together API to access the Perplexity AI model.

This application provides a simple web interface where users can type queries and receive
responses from the Perplexity AI model. The responses are displayed in a highlighted section
on the page, replacing the placeholder text.

Author: Augment AI
Date: May 2025
"""

# Import necessary libraries
from flask import Flask, render_template, request, jsonify, redirect, url_for, session  # Web framework and utilities
import os                                                  # For environment variables
import requests                                            # For making HTTP requests to the API
# json is used implicitly when passing the data parameter to requests.post with json=data
import re                                                  # For regular expressions (used in post-processing)
from dotenv import load_dotenv                             # For loading environment variables from .env file
import secrets                                             # For generating secure tokens

# Load environment variables from .env file
# This allows us to store sensitive information like API keys outside of the code
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = secrets.token_hex(16)  # Generate a random 16-byte hex string as the secret key

# Get Together API key from environment variable
# The API key is used to authenticate requests to the Together API
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")

@app.route('/')
def index():
    """
    Route handler for the home page.

    This function checks if the user has been verified as human.
    If verified, it renders the index.html template.
    If not verified, it redirects to the verification page.

    Returns:
        The rendered HTML template for the home page or a redirect to the verification page.
    """
    # Check if the user has been verified
    if session.get('verified'):
        return render_template('index.html')
    else:
        # Redirect to verification page
        return redirect(url_for('verify_human'))

@app.route('/verify')
def verify_human():
    """
    Route handler for the human verification page.

    This function renders the verify.html template, which displays a GIPHY
    image and asks the user to describe what's happening in the image.

    Returns:
        The rendered HTML template for the verification page.
    """
    return render_template('verify.html')

@app.route('/verify', methods=['POST'])
def process_verification():
    """
    Route handler for processing the verification form submission.

    This function:
    1. Gets the user's answer from the form
    2. Checks if the answer contains keywords related to the GIPHY image
    3. If correct, sets a session variable and redirects to the home page
    4. If incorrect, shows an error message

    Returns:
        A redirect to the home page or the verification page with an error message.
    """
    # Get the answer from the form
    answer = request.form.get('answer', '').lower()

    # Check if the answer contains keywords related to the GIPHY image
    # The GIPHY shows someone falling, so we check for related keywords
    keywords = ['fall', 'falling', 'fell', 'trip', 'tripping', 'slip', 'slipping', 'stumble', 'stumbling']

    # Check if any of the keywords are in the answer
    if any(keyword in answer for keyword in keywords):
        # Set the verified session variable
        session['verified'] = True
        # Redirect to the home page
        return redirect(url_for('index'))
    else:
        # Show an error message
        return render_template('verify.html', error="Incorrect answer. Please try again.")

@app.route('/terms')
def terms():
    """
    Route handler for the Terms of Service page.

    This function checks if the user has been verified as human.
    If verified, it renders the terms.html template.
    If not verified, it redirects to the verification page.

    Returns:
        The rendered HTML template for the Terms of Service page or a redirect to the verification page.
    """
    # Check if the user has been verified
    if session.get('verified'):
        return render_template('terms.html')
    else:
        # Redirect to verification page
        return redirect(url_for('verify_human'))

@app.route('/privacy')
def privacy():
    """
    Route handler for the Privacy Statement page.

    This function checks if the user has been verified as human.
    If verified, it renders the privacy.html template.
    If not verified, it redirects to the verification page.

    Returns:
        The rendered HTML template for the Privacy Statement page or a redirect to the verification page.
    """
    # Check if the user has been verified
    if session.get('verified'):
        return render_template('privacy.html')
    else:
        # Redirect to verification page
        return redirect(url_for('verify_human'))

@app.route('/bypass-verification')
def bypass_verification():
    """
    Route to bypass the human verification (for development purposes).

    This sets the verified session variable to True and redirects to the home page.

    Returns:
        A redirect to the home page.
    """
    # Set the verified session variable
    session['verified'] = True
    # Redirect to the home page
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    """
    Route handler for processing search queries.

    This function:
    1. Checks if the user has been verified as human
    2. Receives the user's query from the form submission
    3. Sends the query to the Together API with a system prompt
    4. Processes the response to remove any thinking tags
    5. Returns the result as JSON for the frontend to display

    Returns:
        JSON response containing either the result or an error message.
    """
    # Check if the user has been verified
    if not session.get('verified'):
        # Return an error message if not verified
        return jsonify({
            "result": "Please verify that you're human before using this service.",
            "error": "Not verified",
            "error_type": "verification_required"
        })

    # Get the query from the form data
    query = request.form.get('query', '')

    # Define the system prompt that guides the AI's responses
    # This prompt instructs the model on how to respond to user queries
    # It focuses on media-related topics and explicitly tells the model not to include thinking tags
    system_prompt = """You are Tolerable, replying to a user query on Tolerable AI.
    Your responses should be informative, balanced, and focused on media topics.
    Focus on themes like:
    - Movies, TV shows, and streaming content
    - Music, albums, and artists
    - Books, authors, and literary works
    - Video games and interactive entertainment
    - Current trends in media and entertainment

    IMPORTANT: DO NOT include any <think> tags, internal monologue, or reasoning process in your response.
    Only provide the direct response to the user.

    Keep responses balanced, thoughtful, and informative. Provide factual information
    while acknowledging different perspectives. Limit responses to 2-3 sentences maximum.
    """

    try:
        # Prepare the API request
        # Set up the headers with authentication and content type
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",  # API key for authentication
            "Content-Type": "application/json"              # Content type for the request
        }

        # Prepare the request data
        # This includes the model to use, the messages to send, and parameters like max_tokens and temperature
        data = {
            "model": "perplexity-ai/r1-1776",  # The AI model to use for generating responses
            "messages": [
                # System message that guides the model's behavior
                {
                    "role": "system",
                    "content": system_prompt
                },
                # User message containing the query
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": 1024,     # Maximum number of tokens in the response
            "temperature": 0.7      # Controls randomness: higher values make output more random
        }

        # Make the API request to the Together API
        # This sends the prepared data to the API endpoint and gets the response
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",  # API endpoint for chat completions
            headers=headers,                                # Headers with API key and content type
            json=data                                       # Request data in JSON format
        )

        # Parse the JSON response from the API
        response_json = response.json()

        # Check if the API request was successful
        # If not, return a calm, relaxed message instead of the technical error
        if response.status_code != 200:
            # Check if it's a rate limit error
            error_message = response_json.get('error', {})
            error_type = error_message.get('type') if isinstance(error_message, dict) else None

            if error_type == 'model_rate_limit' or 'rate limit' in str(error_message).lower():
                # Return a calm message for rate limit errors with error type
                return jsonify({
                    "result": "I'm taking a moment to reflect. The world of media is vast and ever-changing, offering us countless perspectives and experiences to explore. Perhaps we can continue our conversation shortly.",
                    "error": "rate limit",
                    "error_type": "rate_limit"
                })
            else:
                # For other errors, still return a calm message with error type
                return jsonify({
                    "result": "I'm in a contemplative state right now. Media helps us understand ourselves and the world around us in profound ways. Let's explore these ideas again in a moment.",
                    "error": str(error_message),
                    "error_type": "api_error"
                })

        # Extract the result from the response
        # The result is the content of the message from the first choice in the response
        result = response_json["choices"][0]["message"]["content"]

        # Post-process the result to remove any thinking tags or internal monologue
        # This ensures that the response doesn't include any of the model's internal reasoning process
        # We use regular expressions to match and remove different formats of thinking tags
        result = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)           # Remove <think>...</think> tags
        result = re.sub(r'\[thinking\].*?\[/thinking\]', '', result, flags=re.DOTALL)  # Remove [thinking]...[/thinking] tags
        result = re.sub(r'\(thinking\).*?\(/thinking\)', '', result, flags=re.DOTALL)  # Remove (thinking)...(/thinking) tags

        # Return the processed result as JSON
        # This will be sent back to the frontend and displayed to the user
        return jsonify({"result": result})
    except Exception as e:
        # If any error occurs during the process, return a calm, relaxed message
        # This ensures that the user gets a pleasant response even if something goes wrong
        # Include error type for frontend handling
        return jsonify({
            "result": "I'm in a thoughtful mood right now. Media has the power to transform our understanding of the world and connect us across different cultures and experiences. Let's continue our exploration soon.",
            "error": str(e),
            "error_type": "system_error"
        })

# For local development
# This block only runs if the script is executed directly (not imported)
if __name__ == '__main__':
    # Start the Flask development server
    # debug=True enables debug mode, which shows detailed error messages and enables hot reloading
    app.run(debug=True)

# For Vercel deployment
# This exposes the Flask application as a module-level variable
# Vercel looks for this variable to serve the application
app