from flask import Flask, request, jsonify
from functools import wraps
import requests

app = Flask(__name__)

@app.route('/api/v1/certificate/generate')
@auth_required
def generate():
    event_id = request.form['event_id']
    try:
        svg_data = generate_svg(event_id)
        response = {
            "code": 200,
            "message": "success",
            "status": "success",
            "data": {"svg": svg_data} 
        }
    except Exception as error:
        response = {
            "code": 200,
            "message": error,
            "status": "error",
        }
    
    return jsonify(response), 200

def generate_svg(eid):
    # TODO: Generate svg from user data with template
    return None

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = {
            "code": 403,
            "message": "Need Authentication",
            "status": "fail"
        }
        if not '_token' in request.headers:
            return jsonify(response), 403
        else:
            res = requests.get('/api/v1/token/validate',
                data={'token': request.headers['_token']}).json()
            if res['status'] == 'approved':
                return f(*args, **kwargs)
            else:
                return jsonify(response), 403
    return decorated_function
