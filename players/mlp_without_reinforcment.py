class Mlp_without_reinforcment():
    def play_move(self, board):
        mutated = []
        for i in range(9):
            if board[i] == 0:
                mutated.append(0.2)
            elif board[i] == 1:
                mutated.append(0.8)
            elif board[i] == 2:  # 2 is computer
                mutated.append(0.4)
        probabilities = clf.predict_proba([mutated])[0]
        print(probabilities)
        heighest = 0
        index = 0
        for i in range(9):
            if probabilities[i] > heighest and board[i] == 0:
                index = i
                heighest = probabilities[i]
        return index
