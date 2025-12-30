from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from solver import solve_sudoku, validate_board
import copy
import os
import requests

app = Flask(__name__, static_folder='static')
CORS(app)


@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.get_json()
        
        if not data or 'board' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing "board" in request body'
            }), 400
        
        board = data['board']
        
        is_valid, error_msg = validate_board(board)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': f'Invalid board: {error_msg}'
            }), 400
        
        original_board = copy.deepcopy(board)
        
        if solve_sudoku(board):
            return jsonify({
                'success': True,
                'original': original_board,
                'solution': board,
                'message': 'Puzzle solved successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'original': original_board,
                'message': 'No solution exists for this puzzle'
            }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/get-puzzle', methods=['GET'])
def get_puzzle():
    try:
        response = requests.get('https://sudoku-api.vercel.app/api/dosuku', timeout=10)
        
        if response.status_code != 200:
            return jsonify({
                'success': False,
                'message': 'Failed to fetch puzzle from API'
            }), 500
        
        data = response.json()
        
        puzzle_data = data['newboard']['grids'][0]
        puzzle_board = puzzle_data['value']
        solution_board = puzzle_data['solution']
        difficulty = puzzle_data['difficulty']
        
        return jsonify({
            'success': True,
            'board': puzzle_board,
            'solution': solution_board,
            'difficulty': difficulty,
            'message': 'Puzzle loaded successfully'
        }), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'message': f'Network error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Sudoku Solver API'
    }), 200


@app.route('/', methods=['GET'])
def home():
    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)