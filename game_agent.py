"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

DEBUG = False
def debug(*str):
    if DEBUG:
        print(*str)

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player, mode = "schadenfreude"):
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
    elif mode == "mixed_centrality":
        return custom_score_mixed_centrality(game, player)

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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    no_of_moves_left = float(len(game.get_legal_moves(player)))
    space_left = float(len(game.get_blank_spaces()))
    dominance = no_of_moves_left / space_left

    if DEBUG:
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

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)
    no_of_opponents_moves_left = float(len(game.get_legal_moves(opponent)))

    if DEBUG:
        print("no of opponents moves left: ", -no_of_opponents_moves_left)

    return -no_of_opponents_moves_left

def custom_score_dominating_moves(game, player):
    '''
    Expressing the balance between the abilities to move.
    '''
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    no_of_opponents_moves_left = float(len(game.get_legal_moves(opponent)))
    no_of_moves_left = float(len(game.get_legal_moves(player)))
    moves_score = float(1+no_of_moves_left)/(1+(no_of_moves_left+no_of_opponents_moves_left*3)) # 3 = 82.86

    return moves_score

def custom_score_mixed_centrality(game, player):
    '''
    Given that now the actual movement patterns are based on a rook and no
    longer on a queen, the impact of a barrier is not as big anymore. Also
    judging the dominance in space is much harder to calculate efficiently as it
    would need to include trying out the legal moves.

    However staying away from the edges should be a good heuristic. This
    combined with the balance of moves the player has left vs the opponent has
    left (with a small factor added to favor boxing the opponent in), should
    hopefully do well in the tournament. We wil see.
    '''

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)


    no_of_opponents_moves_left = float(len(game.get_legal_moves(opponent)))
    no_of_moves_left = float(len(game.get_legal_moves(player)))
    moves_score = float(1+no_of_moves_left)/(1+(no_of_moves_left+no_of_opponents_moves_left*3)) # 3 = 82.86

    # 1   = 79%
    # 2   = 82%  (81.43%) 82.86%
    # 3   = 79%
    # **2 = 81.43%
    # **3 = 75

    if (game.move_count < 5):
        # 10 81.79
        # 7 80.36
        # 5 86.07
        # 4
        # 2 75.71

        row, col = game.get_player_location(player)
        row -= game.height / 2
        col -= game.width / 2
        row = row**2
        col = row**2
        centrality_raw_score = row*col
        centrality_max_score = (game.height ** 2) * (game.width ** 2)
        centrality_score = 1-(centrality_raw_score / centrality_max_score)

        # *(1/game.move_count+1) Decaying the weight of centrality

        return centrality_score + moves_score*2

    return  moves_score*2

def custom_score_legal_moves_left_balance(game, player):
    '''
    Calculating the score based on the balance between both player's remaining moves.
    If the player under observation has more moves left, then the resulting value should
    be positive, zero if both are equal, and negative otherwise.

    This mechanism is easy to understand and not computational expensive.
    However it needs to collect the remaining moves of **both** players.
    '''

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opponent = game.get_opponent(player)

    no_of_moves_left = float(len(game.get_legal_moves(player)))
    no_of_opponents_moves_left = float(len(game.get_legal_moves(opponent)))

    return no_of_moves_left - no_of_opponents_moves_left

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
        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # MK: This should not happen, bit if we get called without any legal
        # moves to evaluate, then the only logical consequence is to return
        # (-1, -1) as no move is possible
        if not legal_moves:
            return (-1, -1)

        # MK: Pick an arbitrary move, to have something in case of a timeout
        # Otherwise ignoring legal_moves as they are handled in minimax
        # and ab-pruning.

        best = (float('-inf'), legal_moves[0])

        if self.method == 'minimax':
            eval_fun = self.minimax
        else:
            eval_fun = self.alphabeta

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            # --- Iterative
            if self.iterative:

                current_depth = 1 # starting depth
                while self.time_left() > self.TIMER_THRESHOLD:
                    debug("current_depth", current_depth)
                    best = max(best, eval_fun(game, current_depth))

                    # Found a solution?
                    if best[0] in [float("inf"), float("-inf")]:
                        break

                    current_depth += 1
                    # FIXME How about some re-ordering for future extensions here?

            # --- One-Shot
            else:
                debug("not iterative")
                best = max(best, eval_fun(game, self.search_depth))

        except Timeout:
            # Handle any actions required at timeout, if necessary

            # MK: We do not do any explicit checking for a timeout in this
            # method, but rely on the actual work being done in minimax/ab
            # pruning, and we do the time checking there. This allows for more
            # fine grained control, then doing it remotely from here.

            # MK: In case of iterative deepening we do however take time into
            # account on this coarse grained level, before starting a new,
            # deeper search iteration. But even here the cutoff is handled on
            # the work level inside of minimax and ab-pruning.

            pass # MK: Nothing to do here, will return best_move (best[1]) below

        # Return the best move from the last completed search iteration
        return best[1]

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

        # MK: provide margin for debug output reflecting the nested evaluation

        margin = ""
        if DEBUG:
            for x in range(1, 1+self.search_depth-depth):
                margin += "   "

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        debug("\n\n"+margin+"minimax depth: %d max: %s" % (depth, str(maximizing_player)))
        debug(margin + "self.search_depth:"+str(self.search_depth)+" depth: "+ str(depth))


        legal_moves = game.get_legal_moves()
        debug(margin + "legal moves length:"+str(len(legal_moves)))

        v = (float("-inf") if maximizing_player else float("+inf"), (1,1))

        # MK: terminal state?
        if not legal_moves:
            # MK: return the utility of the terminal node
            debug(margin + "terminal state, no legal moves left (%d) or depth (%d) > search_depth (%d)" % (len(legal_moves), depth, self.search_depth))

            v = (game.utility(self), (-1,-1))
            debug(margin + "A returning score: %s next_move: %s" % (v[0], v[1]))

        elif depth == 0:
            v = (self.score(game, self), (-1, -1))

            debug(margin + "B returning score: %s next_move: %s" % (v[0], v[1]))

        else:
            debug(margin + "non-terminal state, depth: %d %d legal moves." % (depth, len(legal_moves)))
            # MK: iterate over the moves / children and look for
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

        # check if terminal node
        # if that is the case use the utility function
          # initialize v to neg infinity (max case)
          #

        margin = ""
        if DEBUG:
            for x in range(1, 1+self.search_depth-depth):
                margin += "   "
        debug(margin+ "============================================================")
        debug(margin+ "abp called with depth: %d alpha: %f beta: %f" %(depth, alpha, beta))
        debug(margin+ "============================================================")

        debug("\n"+margin+"abp depth: %d max: %s" % (depth, str(maximizing_player)))
        debug(margin + "self.search_depth:"+str(self.search_depth)+" depth: "+ str(depth))

        legal_moves = game.get_legal_moves()

        debug(margin + "legal moves length:"+str(len(legal_moves)))

        v = (float("-inf") if maximizing_player else float("+inf"), (1,1))

        # terminal state?
        if not legal_moves:
            # return the utility of the terminal node
            debug(margin + "terminal state, no legal moves left (%d) or depth (%d) > search_depth (%d)" % (len(legal_moves), depth, self.search_depth))

            v = (game.utility(self), (-1,-1))
            debug(margin + "A returning score: %s next_move: %s" % (v[0], v[1]))

        elif depth == 0:
            v = (self.score(game, self), (-1, -1))
            debug(margin + "B returning score: %s next_move: %s" % (v[0], v[1]))

        else:
            debug(margin + "non-terminal state, depth: %d %d legal moves." % (depth, len(legal_moves)))
            # iterate over the moves / children and look for
            # the min/max value

            debug(margin + "is Maximizing:", maximizing_player)

            for move in legal_moves:
                debug(margin + "legal move ", move)
                new_game = game.forecast_move(move)
                new_v = (self.alphabeta(new_game, depth - 1, alpha, beta, not maximizing_player)[0], move)

                evaluated_score, _ = new_v
                debug(margin + "evaluated_score:", evaluated_score, "score:", v[0])
                debug()

                # --- MAX
                if maximizing_player:
                    if evaluated_score >= beta:
                        debug(margin + "pruning")
                        #continue # MK: pruning as min would not pick this move
                        return new_v

                    if evaluated_score > alpha:
                        debug(margin + "alpha updated")
                        alpha = evaluated_score

                    if evaluated_score > v[0]:
                        v = new_v


                # --- MIN
                else:
                    if evaluated_score <= alpha:
                        debug(margin + "pruning")
                        #continue # MK: pruning here as well
                        return new_v

                    if evaluated_score < beta:
                        debug(margin + "beta updated")
                        beta = evaluated_score

                    if evaluated_score < v[0]:
                        v = new_v

                #best = max if maximizing_player else min
                #v = best(v, new_v)

                debug(margin + "C returning score: %s next_move: %s" % (v[0], v[1]))
        return v
