from engine import Vector2
import engine

def main() -> None:
    screen = engine.Screen(
        Vector2(0, 0),
        Vector2(-10, -10)
    )
    game: engine.GameLoop = engine.GameLoop(screen, 60)
    game.run()

    for i in range(len(screen.pole[0])):
        game.addObject(
            engine.Object(
                str(i),
                Vector2(-i, 0),
                cells=[
                    engine.Cell(
                        Vector2(-i, 0),
                        engine.Symbols.F
                    )
                ]
            )
        )
        engine.time.sleep(1)
    game.stop()
main()
