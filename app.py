from flask import Flask,render_template, request, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

boggle_game = Boggle()

@app.route("/")
def home_page():
    """"Show home page with game instructions and a button to start game"""
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    """
    Start game,display board of letters, keep track of games played in session as session["games"]
    """
    # generate board to display
    board = boggle_game.make_board()
    # add board to session
    session['board'] = board
    # check if games is already in session and increment, otherwise initialize to 1
    if "games" in session:
        session["games"] += 1
    else:
        session["games"] = 1
    return render_template("start.html", board=board)

@app.route("/validate_guess", methods=["POST"])
def validate_guess():
    """Check that word guessed is a valid word and that it exists in the dictionary, return a response with the word and response according to conditions
    
        if word_exists and valid_word:
            result = 'ok'
        elif word_exists and not valid_word:
            result = 'not-on-board'
        else:
            result = 'not-word'    
            
    """
    # retrieve guess from json request
    guess = request.json.get("guess")
    # keep track of board in session
    board = session["board"]
    # set the result to a variable
    result = boggle_game.check_valid_word(board, guess)
    #  return to JSON to frontend
    return jsonify({'result': result, "word":guess})

@app.route("/game_over", methods=["POST"])
def update_game_stats():
    """Keep track of highest score so far, update the number of games played"""
    
    # retrieve game score
    gameScore = request.json.get("gameScore")
    
    # get current number of games played from session, set to zero if no games played previously
    gamesPlayed = session.get("games", 0)
    
    # Increment gamesPlayed and set it in the session
    gamesPlayed += 1
    session["games"] = gamesPlayed

    #add or update high score
    if "high_score" in session:
        if gameScore > session["high_score"]:
            session["high_score"] = gameScore 
    else:
        session["high_score"] = gameScore
        
    current_high_score = session["high_score"]
    
    # send response with games played and high score to display to user
    return jsonify({"games": gamesPlayed, "high_score": current_high_score})

        
    