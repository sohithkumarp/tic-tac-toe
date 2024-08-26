from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize game state
board = [' '] * 9
current_player = 'X'
game_over = False

def check_winner():
    # Winning combinations
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:
        return "Draw"
    return None

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({"board": board, "current_player": current_player, "game_over": game_over})

@app.route('/move', methods=['POST'])
def make_move():
    global current_player, game_over
    if game_over:
        return jsonify({"error": "Game is already over."}), 400

    data = request.json
    position = data.get('position')

    if board[position] != ' ':
        return jsonify({"error": "Position already taken."}), 400

    board[position] = current_player
    winner = check_winner()

    if winner:
        game_over = True
        if winner == "Draw":
            return jsonify({"message": "The game is a draw.", "board": board})
        else:
            return jsonify({"message": f"Player {winner} wins!", "board": board})

    # Switch player
    current_player = 'O' if current_player == 'X' else 'X'
    return jsonify({"board": board, "current_player": current_player})

@app.route('/reset', methods=['POST'])
def reset_game():
    global board, current_player, game_over
    board = [' '] * 9
    current_player = 'X'
    game_over = False
    return jsonify({"message": "Game reset successful.", "board": board})

if __name__ == '__main__':
    app.run(debug=True)
