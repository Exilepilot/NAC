"""
Contains the minimax algorithm.
"""
from game.Board import Board
from game.Locals import *

__MOVE = None

def get_move(board, max_depth, comp_peice, player_peice):
    #TODO Test
    """
    Retrieve the best move found by the minimax algorithm.
    Params: max_depth, the maximum recursion depth for the minimax algorithm.
            comp_peice, the peice used by the computer.
            player_peice, the peice used by the player.
    """
    minimax(board, 0, max_depth, comp_peice, player_peice)
    return __MOVE

def score(board, comp_peice):
    #TODO Test
    """
    Computes a score from the game board from the eyes of the computer AI.
    Params: comp_peice, the computers peice on the board.
    Params: board, The board object to compute on.
    Returns: int score.
    """
    coeff = [1, 1, 100]
    max_score = 0
    for i in range(3):
        # i + 1, since i starts at 0.
        max_score += coeff[i] * board.find(comp_peice, i + 1)

    return max_score

def minimax(board, depth, max_depth, comp_peice, player_peice):
    #TODO: Description
    #TODO: Test
    """
    """
    global __MOVE
    current_peice = comp_peice if depth % 2 == 0 else player_peice

    if depth >= max_depth or board.game_over:
        return score(board, comp_peice)

    scores = []
    moves = []

    for move in board.possible_moves():
        board.place_move(current_peice, move)
        scores.append(minimax(board, depth + 1, max_depth, comp_peice, player_peice))
        moves.append(move)
        board.revert_move(move)

    if current_peice == comp_peice:
        max_score_index = scores.index(max(scores))
        __MOVE = moves[max_score_index]
        return scores[max_score_index]
    else:
        min_score_index = scores.index(min(scores))
        __MOVE = moves[min_score_index]
        return scores[min_score_index]
