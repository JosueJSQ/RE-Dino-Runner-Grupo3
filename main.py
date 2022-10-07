from dino_runner.components.game import Game
if __name__ == "__main__":
     game=Game()
     while game.running:
          game.show_menu()          
          if not game.playing:
               game.show_menu()
               

