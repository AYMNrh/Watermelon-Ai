import random
import math
from datetime import datetime
import os

# Game settings
screen_width = 600
screen_height = 800
limit_height = 600  # Height limit for game over
gravity = 0.05
num_moves = 5  # Number of balls to drop
skewed_probability = [0.7, 0.1, 0.05, 0.08, 0.04, 0.02, 0.01, 0, 0]
# skewed_probability = [0, 0, 0, 0, 0, 0, 0, 0, 1]  # Only purple balls

# Ball properties
color_order = ['white', 'red', 'orange', 'yellow', 'green', 'blue', 'thistle', 'hot_pink', 'purple']
score_order = [0, 2, 4, 8, 8, 16, 32, 64, 128]
radius_order = [15, 22, 42, 55, 68, 85, 94, 110, 130]

# Initialize game variables
score = 0
balls = []
game_over = False
log_directory = "game_logs"  # Specify the directory path here for logs to be saved
log_filename = os.path.join(log_directory, f"game_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")


def log_game(message):
    with open(log_filename, "a") as log_file:
        log_file.write(message + "\n")

def add_ball():
    color_index = random.choices(range(len(color_order)), weights=skewed_probability, k=1)[0]
    ball_x = random.randint(40 + radius_order[color_index], 560 - radius_order[color_index])
    ball_y = 40 + radius_order[color_index]
    ball = {'x': ball_x, 'y': ball_y, 'vy': 0, 'color': color_order[color_index], 'radius': radius_order[color_index]}
    balls.append(ball)
    log_game(f"Added ball: Color={ball['color']}, Position=({ball['x']}, {ball['y']})")
    return ball

def update_physics():
    global score, game_over
    for ball in balls:
        ball['y'] += ball['vy']
        ball['vy'] += gravity

        # Ball stops at the bottom of the screen
        if ball['y'] + ball['radius'] >= screen_height - 40:
            ball['y'] = screen_height - 40 - ball['radius']
            ball['vy'] = 0

        # Check for game over condition: Ball crosses the height limit
        if ball['y'] - ball['radius'] < limit_height:
            game_over = True
            return "Game Over"

    # Improved collision and merging code
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1, ball2 = balls[i], balls[j]
            dx, dy = ball1['x'] - ball2['x'], ball1['y'] - ball2['y']
            distance = math.sqrt(dx**2 + dy**2)
            if distance < ball1['radius'] + ball2['radius']:
                if ball1['color'] == ball2['color']:
                    color_index = color_order.index(ball1['color'])
                    if color_index + 1 < len(color_order):
                        merged_ball = {'x': (ball1['x'] + ball2['x']) / 2, 
                                       'y': (ball1['y'] + ball2['y']) / 2, 
                                       'vy': 0, 
                                       'color': color_order[color_index + 1], 
                                       'radius': radius_order[color_index + 1]}
                        balls.append(merged_ball)
                        balls.remove(ball1)
                        balls.remove(ball2)
                        score += score_order[color_index + 1]
                        log_game(f"Merged balls to form a {merged_ball['color']} ball.")
                        # Check for game over condition after merging
                        if merged_ball['y'] - merged_ball['radius'] < limit_height:
                            game_over = True
                            return "Game Over"
                        return None

    return None

def print_game_state():
    state_message = f"Current Score: {score}\n"
    for ball in balls:
        state_message += f"Ball {ball['color']} at ({ball['x']}, {ball['y']})\n"
    print(state_message)
    log_game(state_message)

# Main game loop
for move in range(num_moves):
    if game_over:
        remaining_moves = num_moves - move
        log_game(f"Game Over! A ball has crossed the height limit. Remaining Moves: {remaining_moves}")
        print(f"Game Over! A ball has crossed the height limit. Remaining Moves: {remaining_moves}")
        break
    new_ball = add_ball()
    
    # Update physics and check for collisions
    collision = True
    while collision:
        collision = update_physics()
        if collision == "Game Over":
            remaining_moves = num_moves - move
            log_game(f"Game Over! A ball has crossed the height limit. Remaining Moves: {remaining_moves}")
            print(f"Game Over! A ball has crossed the height limit. Remaining Moves: {remaining_moves}")
            break
        print_game_state()

# Log and print game finish status
if not game_over:
    log_game("Game finished naturally. Final Score: " + str(score))
    print("Game finished naturally. Final Score: " + str(score))