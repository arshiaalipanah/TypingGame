def calculate_elo(player1_elo, player2_elo, winner: int, k=32):
    """
    winner = 1 if player1 wins, 2 if player2 wins
    """
    # Expected scores
    expected1 = 1 / (1 + 10 ** ((player2_elo - player1_elo) / 400))
    expected2 = 1 / (1 + 10 ** ((player1_elo - player2_elo) / 400))

    if winner == 1:
        score1, score2 = 1, 0
    else:
        score1, score2 = 0, 1

    new_elo1 = player1_elo + k * (score1 - expected1)
    new_elo2 = player2_elo + k * (score2 - expected2)

    return round(new_elo1), round(new_elo2)