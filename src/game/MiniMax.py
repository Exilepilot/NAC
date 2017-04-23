"""
Contains the minimax algorithm.
"""
from game.Board import Board
from game.Locals import *


__MOVE = None

def get_move(board, max_depth):
    minimax(board, 0, max_depth)
    return __MOVE


def score(board):
    """
    Computes a score from the game board from the eyes of the computer AI.
    :param board: The board object to compute.
    :param maxPlayer: The player playing as the computer AI.
    :return: Integer value, score.
    """
    #assert isinstance(board, Board)

    coeff = [1, 1, 100]
    max_score = 0
    for i in range(3):
        max_score += coeff[i] * board.find(PLAYER_TWO, i + 1)

    # min_score = 0
    # for i in range(3):
    #     min_score += coeff[i] * board.find(PLAYER_TWO, i + 1)


    return max_score


def minimax(board, depth, max_depth):
    global __MOVE
    current_player = PLAYER_TWO if depth % 2 == 0 else PLAYER_ONE

    # MAX_DEPTH of 3 seems to work the best.
    if depth >= max_depth or board.game_over:
        return score(board)

    scores = []
    moves = []

    for move in board.possible_moves():
        board.place_move(current_player, move)
        scores.append(minimax(board, depth + 1, max_depth))
        moves.append(move)
        board.revert_move(move)

    if current_player == PLAYER_TWO:
        max_score_index = scores.index(max(scores))
        __MOVE = moves[max_score_index]
        return scores[max_score_index]
    else:
        min_score_index = scores.index(min(scores))
        __MOVE = moves[min_score_index]
        return scores[min_score_index]
