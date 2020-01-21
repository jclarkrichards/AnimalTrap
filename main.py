from gamerules import AnimalTrap

game = AnimalTrap()
game.setPlayers()
print(game.template)
print("==================")

while not game.gameover:
    print(game.state)
    print("Player " + str(game.player) + " move")
    if game.player == 1:
        if game.player1Human:
            values = game.getHumanChoice()
            game.setState(values)
        else:
            game.setNextStateAuto()
    else:
        if game.player2Human:
            values = game.getHumanChoice()
            game.setState(values)
        else:
            game.setNextStateAuto()

    
    game.checkEndGame()
    game.setPlayer()    
    #game.nextTurn()

print("GAME OVER MAN!")
print("")
print(game.state)
