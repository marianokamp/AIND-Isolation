"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

DEBUG = False
def debug(str = ""):
    if DEBUG: print(str)

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player, mode = "lmlb"):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if mode == "lmlb":
        return custom_score_legal_moves_left_balance(game, player)
    elif mode == "ds":
        return custom_score_dominating_space(game, player)
    elif mode == "schadenfreude":
        return custom_score_schadenfreude(game, player)

def custom_score_dominating_space(game, player):
    '''
    Calculating the score based on the relative dominance of the current
    player with respect to the available space.

    Here the current players remaining moves are compared to remaining blank
    spaces. Strictly speaking this is an apples to oranges comparison, because
    not all spaces may be reachable given the movement pattern - two moves in
    one direction and one move in another - but this is just one of many
    heuristics and could be enhanced by changing to a more exact method, when
    only five spaces are remaining.

    This method ignores the opponent's position. It could be extended to run
    this for the opponent as well and then express it as a balance or ratio.

    A positive value indicates a dominace of the current player.
    '''

    game.get_blank_spaces

    no_of_moves_left = float(len(game.get_legal_moves(player)))
    space_left = float(len(game.get_blank_spaces()))
    dominance = no_of_moves_left / space_left

    print("dominance", dominance, "moves", no_of_moves_left, "space", space_left)

    return dominance

def custom_score_schadenfreude(game, player):
    '''
    Calculating the score by putting an emphasis on limiting the other player's
    inability to move.

    The current implementation is laser sharp focused on the opponent only.
    A more balanced implementation could take the current players possible moves
    into account as well. Maybe: -opponent_moves*2+own_moves
    '''

    opponent = game.get_opponent(player)
    no_of_opponents_moves_left = float(len(game.get_legal_moves(opponent)))

    print("no of opponents moves left: ", -no_of_opponents_moves_left)

    return -no_of_opponents_moves_left

def custom_score_legal_moves_left_balance(game, player):
    '''
    Calculating the score based on the balance between both player's remaining moves.
    If the player under observation has more moves left, then the resulting value should
    be positive, zero if both are equal, and negative otherwise.

    This mechanism is easy to understand and not computational expensive.
    However it needs to collect the remaining moves of **both** players.

    '''

    opponent = game.get_opponent(player)

    no_of_moves_left = float(len(game.get_legal_moves(player)))
    print(game.get_legal_moves(player)) # FIXME
    no_of_opponents_moves_left = float(len(game.get_legal_moves(opponent)))
    print(game.get_legal_moves(opponent)) # FIXME

    print(no_of_moves_left, no_of_opponents_moves_left) # FIXME

    return no_of_moves_left - no_of_opponents_moves_left


def custom_score_template(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    raise NotImplementedError

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            DEPRECATED -- This argument will be removed in the next release

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            pass

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        raise NotImplementedError

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """

        # provide margin for debug output reflecting the nested evaluation
        if DEBUG:
            margin = ""
            for x in range(1, 1+self.search_depth-depth):
                margin += "   "

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        debug("\n\n"+margin+"minimax depth: %d max: %s" % (depth, str(maximizing_player)))
        debug(margin + "self.search_depth:"+str(self.search_depth)+" depth: "+ str(depth))


        legal_moves = game.get_legal_moves()
        debug(margin + "legal moves length:"+str(len(legal_moves)))

        v = (float("-inf") if maximizing_player else float("+inf"), (1,1))

        # terminal state?
        if not legal_moves:
            # return the utility of the terminal node
            debug(margin + "terminal state, no legal moves left (%d) or depth (%d) > search_depth (%d)" % (len(legal_moves), depth, self.search_depth))

            # update utility, leave -1, -1
            v = (game.utility(self), (-1,-1))
            debug(margin + "A returning score: %s next_move: %s" % (v[0], v[1]))

        elif depth == 0:
            v = (self.score(game, self), (-1, -1))

            debug(margin + "B returning score: %s next_move: %s" % (v[0], v[1]))

        else:
            debug(margin + "non-terminal state, depth: %d %d legal moves." % (depth, len(legal_moves)))
            # iterate over the moves / children and look for
            # the min/max value

            for move in legal_moves:
                debug(margin + "legal move "+str(move))
                new_game = game.forecast_move(move)
                new_v = (self.minimax(new_game, depth - 1, not maximizing_player)[0], move)

                debug()

                best = max if maximizing_player else min
                v = best(v, new_v)

                debug(margin + "C returning score: %s next_move: %s" % (v[0], v[1]))
        return v




    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        raise NotImplementedError
