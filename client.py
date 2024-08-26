import requests

BASE_URL = 'http://127.0.0.1:5000'

def display_board(board):
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print("--|---|--")

def get_board():
    response = requests.get(f'{BASE_URL}/board')
    data = response.json()
    display_board(data['board'])
    if data['game_over']:
        print("Game Over!")
    else:
        print(f"Current Player: {data['current_player']}")

def make_move(position):
    response = requests.post(f'{BASE_URL}/move', json={"position": position})
    if response.status_code == 200:
        data = response.json()
        display_board(data['board'])
        if 'message' in data:
            print(data['message'])
    else:
        print(f"Error: {response.json()['error']}")

def reset_game():
    response = requests.post(f'{BASE_URL}/reset')
    print(response.json()['message'])

if __name__ == '__main__':
    print("Welcome to Tic-Tac-Toe!")
    while True:
        get_board()
        move = input("Enter position (0-8) or 'r' to reset the game: ")
        if move.lower() == 'r':
            reset_game()
        elif move.isdigit() and 0 <= int(move) <= 8:
            make_move(int(move))
        else:
            print("Invalid input. Try again.")
