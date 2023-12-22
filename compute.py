import random
import math

# Constants and initialization
screen_width = 600
screen_height = 800
agent_moves = 1000
skewed_probability = [0.7, 0.1, 0.05, 0.08, 0.04, 0.02, 0.01, 0, 0]
color_order = ['white', 'red', 'orange', 'yellow', 'green', 'blue', 'thistle', 'hot_pink', 'purple']
radius_order = [15, 22, 42, 55, 68, 85, 94, 110, 130]
score_order = [0, 2, 4, 8, 8, 16, 32, 64, 128]
gravity = 10
balls = []
score = 0

# Function definitions
def agent_move():
    index_range = range(len(color_order))
    random_int = random.choices(index_range, weights=skewed_probability, k=1)[0]
    x = random.randint(40, screen_width - 40)
    y = 40  # y-coordinate is fixed at the top
    color = color_order[random_int]
    radius = radius_order[random_int]
    balls.append([x, y, 0, 0, color, radius, True])  # Horizontal speed and dropping flag
    return f"Agent dropped a {color} ball at ({x}, {y})"


def check_collision():
    global score
    balls_to_remove = []
    balls_to_add = []
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            dx = balls[i][0] - balls[j][0]
            dy = balls[i][1] - balls[j][1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < balls[i][5] + balls[j][5]:
                if balls[i][4] == balls[j][4]:  # Same color
                    color_index = color_order.index(balls[i][4])
                    if color_index + 1 < len(color_order):
                        new_x = (balls[i][0] + balls[j][0]) // 2
                        new_y = (balls[i][1] + balls[j][1]) // 2
                        new_color = color_order[color_index + 1]
                        new_radius = radius_order[color_index + 1]
                        balls_to_add.append([new_x, new_y, 0, 0, new_color, new_radius, False])
                        score += score_order[color_index + 1]
                        balls_to_remove.extend([balls[i], balls[j]])
                        print(f"Balls collided and merged into a {new_color} ball")
                        
                    else:
                        score += score_order[color_index] * 2
    return balls_to_remove, balls_to_add

# Main simulation loop
game_over = False
while not game_over and agent_moves > 0:
    agent_move_info = agent_move()
    print(agent_move_info)
    agent_moves -= 1

    # Update balls' positions and check for game over
    for ball in balls:
        ball[1] += gravity  # Apply gravity
        if ball[1] >= screen_height - ball[5]:
            game_over = True
            print("Game Over: A ball reached the top line")
    
    # Check for collisions and update score
    balls_to_remove, balls_to_add = check_collision()
    for ball in balls_to_remove:
        balls.remove(ball)
    balls.extend(balls_to_add)

    # Print the current state of the game
    print(f"Current score: {score}")
    for ball in balls:
        print(f"Ball at ({ball[0]}, {ball[1]}) with color {ball[4]}")

if not game_over:
    print("Game ended with all agent moves used")
print(f"Final Score: {score}")
