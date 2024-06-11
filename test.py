from ext.Vector import Vector2, Cell
from ext.KeyListener import Keys
from ext.Vector import Vector2, Cell
from ext.Event import Events, Event, Bindable
from ext.GameObject import Object
import time
import cep

class GameConfig():
    screenWidth  = 10
    screenHeight = 10
    playerSpeed  = 1
    FPS = 60

class Game(cep.GameLoop):
    def __init__(
        self,
        screen: cep.Screen,
        fps: cep.V = 1
    ) -> None:
        super().__init__(screen, fps)
        # Init objects
        # Init player
        self.addObject(
            "player",
            Vector2(GameConfig.screenWidth//2, GameConfig.screenHeight//2)
        )
        self.objects["player"].cells = [
            Cell(Vector2(GameConfig.screenWidth//2, GameConfig.screenHeight//2), symbol=cep.Symbols.PLAYER)
        ]
        # Init border
        self.addObject(
            "border",
            Vector2(0, 0)
        )
        self.objects["border"].cells.extend([Cell(Vector2(-x, 0), cep.Symbols.BORDER) for x in range(0, GameConfig.screenWidth)])
        self.objects["border"].cells.extend([Cell(Vector2(-x, -9), cep.Symbols.BORDER) for x in range(0, GameConfig.screenWidth)])
        self.objects["border"].cells.extend([Cell(Vector2(0, -y), cep.Symbols.BORDER) for y in range(0, GameConfig.screenHeight)])
        self.objects["border"].cells.extend([Cell(Vector2(-9, y), cep.Symbols.BORDER) for y in range(0, GameConfig.screenHeight)])
    
    def updating(self, gameLoop: cep.GameLoop = None) -> None:
        while self.running:
            if Keys.right:
                self.objects["player"].move(Vector2(-GameConfig.playerSpeed, 0))
                Keys.right = False

            if Keys.left:
                self.objects["player"].move(Vector2(GameConfig.playerSpeed, 0))
                Keys.left = False

            if Keys.up:
                self.objects["player"].move(Vector2(0, GameConfig.playerSpeed))
                Keys.up = False

            if Keys.down:
                self.objects["player"].move(Vector2(0, -GameConfig.playerSpeed))
                Keys.down = False

            self.redraw(self.objects)
            time.sleep(1 / self.fps)
            self.screen.update()

def main():
    screen = cep.Screen(GameConfig.screenWidth, GameConfig.screenHeight)
    game = Game(screen, fps=GameConfig.FPS)
    game.run()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        game.stop()

if __name__ == "__main__":
    main()