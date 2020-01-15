from gamerules import AnimalTrap

game = AnimalTrap()
game.setPlayers()
print(game.template)
print("==================")

while not game.gameover:
    if game.xturn:
        print("X PLAYER")
        if game.xplayer:
            if firstTurn:
                index = game.humanFirstTurn()
                game.startState[index] = 'X'
                game.setupTree()
            else:
                game.humanTurn('X')
        else:
            if firstTurn:
                index = 4
                game.startState[index] = 'X'
                game.setupTree()
            else:
                minimax = Minimax(game.tree)
                index = minimax.findBestMove('X')
                game.makeMoveAI(index)
    else:
        print("O PLAYER")
        if game.oplayer:
            game.humanTurn('O')
        else:
            minimax = Minimax(game.tree)
            index = minimax.findBestMove('O')
            game.makeMoveAI(index)
            
    print(game.tree.root.data)
    firstTurn = False
    if game.checkEndGame():
        game.gameover = True
    game.xturn = not game.xturn

print("GAME OVER MAN!")
