import pygame
import sys
import math
from utils.robot import Robot

# --- Konstanta ---
WIDTH, HEIGHT = 1200, 700
PATH_COLOR = (0, 0, 0)
PATH_THICKNESS = 25

def build_path():
    path_points = []
    for x in range(0, 151, 10):  
        path_points.append((x, HEIGHT // 2))

    for x in range(150, WIDTH + 1, 10):  
        y = (HEIGHT // 2) + 120 * math.sin((x - 150) / 200)
        path_points.append((x, int(y)))

    return path_points

def on_line(screen, pos):
    x, y = pos
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        return screen.get_at((x, y))[:3] == PATH_COLOR
    return False

def main():
    # --- Setup Pygame ---
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Line Follower Robot")
    clock = pygame.time.Clock()

    robot = Robot(50, HEIGHT // 2)

    path_points = build_path()

    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        pygame.draw.lines(screen, PATH_COLOR, False, path_points, PATH_THICKNESS)

        left, right = robot.get_sensors()
        left_on_line = on_line(screen, left)
        right_on_line = on_line(screen, right)
        
        robot.update_state(left_on_line, right_on_line)
        robot.move()
        robot.draw(screen)

        font = pygame.font.SysFont(None, 24)
        text_state = font.render(f"State: {robot.state.name}", True, (0, 0, 0))
        text_event = font.render(f"Event: {robot.event.name}", True, (0, 0, 0))
        screen.blit(text_state, (10, 10))
        screen.blit(text_event, (10, 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()