import pygame
import serial

pygame.init()

win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Joystick Game")

char_size = 50
char_color = (0, 255, 0)
char_x, char_y = win_width // 2, win_height // 2
char_speed = 5

arduino_port = 'COM5'
ser = serial.Serial(arduino_port,9600)

running = True

prev_x, prev_y = char_x, char_y

button_state = 0  # Initialize button_state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Correct assignment

    data = ser.readline().decode().strip().split(',')

    if len(data) == 3 and all(item.isdigit() for item in data):
        joy_x, joy_y, button_state = map(int, data)
        print(f"X:{joy_x}, Y: {joy_y}, Button: {button_state}")

        new_x = char_x + (joy_x - 512) // 100 * char_speed
        new_y = char_y + (joy_y - 512) // 100 * char_speed

        new_x = max(char_size // 2, min(win_width - char_size // 2, new_x))
        new_y = max(char_size // 2, min(win_height - char_size // 2, new_y))

        if (new_x, new_y) != (prev_x, prev_y):
            char_x, char_y = new_x, new_y
            prev_x, prev_y = char_x, char_y

    char_color = (0, 0, 255) if button_state == 1 else (255, 0, 0)

    win.fill((255, 255, 255))
    pygame.draw.circle(win, char_color, (char_x, char_y), char_size // 2)
    pygame.display.flip()

ser.close()
pygame.quit()