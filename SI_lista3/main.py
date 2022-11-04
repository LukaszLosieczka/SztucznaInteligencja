import checkers
import human_player
import bot_player


def save_to_file(depth, time, nodes, file):
    file = open(file, "a")
    file.write(f"\n{depth}\t\t\t{round(time, 3)}\t\t\t{round(nodes)}")
    file.close()


def tests(number_of_repetition):
    file = open("min_max_stats.txt", "w")
    file.write("depth\t\ttime\t\tnodes")
    file.close()
    file = open("alpha_beta_stats.txt", "w")
    file.write("depth\t\ttime\t\tnodes")
    file.close()
    for depth in range(7, 8):
        time_sum_min_max = 0
        nodes_sum_min_max = 0
        time_sum_alpha_beta = 0
        nodes_sum_alpha_beta = 0
        for j in range(number_of_repetition):
            checkers_board = checkers.Board(8, pawns_rows=2)
            player_min_max = bot_player.MinMaxBotPlayer("player5 - min/max bot", depth)
            player_alpha_beta = bot_player.AlfaBetaBotPlayer("player6 - alpha/beta bot", depth)
            checkers.Checkers(player_min_max, player_alpha_beta, checkers_board).start_game()
            time_sum_min_max += player_min_max.time_stats["time_sum"]/player_min_max.time_stats["measurements_no"]
            time_sum_alpha_beta += player_alpha_beta.time_stats["time_sum"]/player_min_max.time_stats["measurements_no"]
            nodes_sum_min_max += player_min_max.node_stats["nodes_sum"]/player_min_max.node_stats["measurements_no"]
            nodes_sum_alpha_beta += player_alpha_beta.node_stats["nodes_sum"]/player_min_max.node_stats["measurements_no"]
        save_to_file(depth, time_sum_min_max/number_of_repetition, nodes_sum_min_max/number_of_repetition,
                     "min_max_stats.txt")
        save_to_file(depth, time_sum_alpha_beta / number_of_repetition, nodes_sum_alpha_beta / number_of_repetition,
                     "alpha_beta_stats.txt")


if __name__ == '__main__':
    board = checkers.Board(8, pawns_rows=2)
    player1 = human_player.HumanPlayer("player1 - human")
    player2 = bot_player.RandomBotPlayer("player2 - random bot")

    player3 = bot_player.MinMaxBotPlayer("player3 - min/max bot", 5)
    player4 = bot_player.MinMaxBotPlayer("player4 - min/max bot", 6)

    player5 = bot_player.AlfaBetaBotPlayer("player5 - alpha/beta bot", 3)
    player6 = bot_player.AlfaBetaBotPlayer("player6 - alpha/beta bot", 6)
    player7 = human_player.HumanPlayer("player7 - human")

    checkers.Checkers(player4, player6, board).start_game()
    # min/max stats
    avg_time1 = player4.time_stats["time_sum"] / player4.time_stats["measurements_no"]
    avg_nodes1 = player4.node_stats["nodes_sum"] / player4.node_stats["measurements_no"]
    print(f"\n{player4.name} stats: ")
    print(f"avg time per move: {round(avg_time1, 2)} s")
    print(f"avg nodes per move: {round(avg_nodes1)}")
    # alpha/beta stats
    avg_time2 = player6.time_stats["time_sum"] / player6.time_stats["measurements_no"]
    avg_nodes2 = player6.node_stats["nodes_sum"] / player6.node_stats["measurements_no"]
    print(f"\n{player6.name} stats: ")
    print(f"avg time per move: {round(avg_time2, 2)} s")
    print(f"avg nodes per move: {round(avg_nodes2)}")
