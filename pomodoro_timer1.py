#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Copyright (c) 2025 Shawn Lokshin
# Licensed under the MIT License.

import time
import sys
import pygame
from plyer import notification
import webbrowser

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load the icon for the window (make sure the file is in the same directory or provide full path)
icon = pygame.image.load("pomodoro_25_5.png")  # Replace with your tomato image filename
pygame.display.set_icon(icon)

# Screen dimensions
global screen_width, screen_height
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Task Master: Pomodoro Timer")

# Use a cyberpunk-style font, Orbitron
font = pygame.font.Font("Orbitron-Regular.ttf", 24)  # You need to download the font file
big_font = pygame.font.Font("Orbitron-Regular.ttf", 72)

# Colors (Neon and cyberpunk-style colors)
WHITE, NEON_GREEN, NEON_PINK, NEON_BLUE, BLACK = (255, 255, 255), (57, 255, 20), (255, 20, 147), (0, 255, 255), (18, 18, 18)

# Global variables
work_time, break_time = 25 * 60, 5 * 60  # Default values
current_time = work_time
is_break_time, running, paused = False, False, False
on_timer_page = False  # Tracks whether the user is on the timer page
input_focus = "work"  # Tracks which input field is focused (work or break)
work_input, break_input = "", ""  # User input storage

def show_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def send_notification(message):
    notification.notify(
        title='Pomodoro Timer',
        message=message,
        timeout=10
    )

def open_sponsor_page():
    webbrowser.open("http://example.com")

def run_timer():
    global current_time, is_break_time, running, paused, screen, screen_width, screen_height
    last_time = time.time()

    while running:
        screen.fill(BLACK)
        minutes, seconds = int(current_time // 60), int(current_time % 60)
        # Adjusted timer position to perfectly center
        show_text(f"{minutes:02}:{seconds:02}", screen_width // 2 - big_font.size(f"{minutes:02}:{seconds:02}")[0] // 2, screen_height // 2 - big_font.get_height() // 2, big_font, NEON_BLUE)

        # Sponsor link (bottom of the screen)
        show_text("Powered by example.com", screen_width // 2 - font.size("Powered by example.com")[0] // 2, screen_height - 50, font, NEON_GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the sponsor link is clicked
                sponsor_rect = pygame.Rect(screen_width // 2 - font.size("Powered by example.com")[0] // 2, screen_height - 50, font.size("Powered by example.com")[0], font.get_height())
                if sponsor_rect.collidepoint(event.pos):
                    open_sponsor_page()

        if not paused and current_time > 0:
            current_time -= time.time() - last_time
            last_time = time.time()

        if current_time <= 0:
            if is_break_time:
                current_time, is_break_time = work_time, False
                send_notification("Time to work!")
            else:
                current_time, is_break_time = break_time, True
                send_notification("Take a break!")

        pygame.display.update()

def start_timer():
    global running, paused
    running, paused = True, False
    run_timer()

def first_page():
    global work_time, break_time, on_timer_page, input_focus, work_input, break_input, screen, screen_width, screen_height
    cursor_visible = True
    cursor_timer = 0

    while True:
        screen.fill(BLACK)
        show_text("Enter Work Time (minutes):", 50, 50, font, NEON_GREEN)
        show_text("Enter Break Time (minutes):", 50, 150, font, NEON_GREEN)

        work_rect, break_rect = pygame.Rect(50, 100, 200, 40), pygame.Rect(50, 200, 200, 40)
        pygame.draw.rect(screen, NEON_PINK if input_focus == "work" else NEON_BLUE, work_rect, 2)
        pygame.draw.rect(screen, NEON_PINK if input_focus == "break" else NEON_BLUE, break_rect, 2)
        show_text(work_input, 60, 110, font, WHITE)
        show_text(break_input, 60, 210, font, WHITE)

        cursor_timer += 1
        if cursor_timer > 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        if cursor_visible:
            cursor_x = 60 + font.size(work_input if input_focus == "work" else break_input)[0]
            pygame.draw.line(screen, WHITE, (cursor_x, 110 if input_focus == "work" else 210), (cursor_x, 140 if input_focus == "work" else 240), 2)

        start_button = pygame.Rect(250, 350, 120, 50)
        pygame.draw.rect(screen, NEON_BLUE, start_button)
        show_text("Start", 275, 360, font, WHITE)

        # Sponsor button (first page)
        sponsor_button = pygame.Rect(250, 450, 140, 50)
        pygame.draw.rect(screen, NEON_GREEN, sponsor_button)
        show_text("Sponsor", 265, 460, font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.SCALED)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if work_rect.collidepoint(event.pos):
                    input_focus = "work"
                elif break_rect.collidepoint(event.pos):
                    input_focus = "break"
                elif start_button.collidepoint(event.pos):
                    if work_input.isdigit() and break_input.isdigit():
                        work_time, break_time = int(work_input) * 60, int(break_input) * 60
                        global current_time
                        current_time = work_time
                        on_timer_page = True
                        return  
                # Check if the sponsor button is clicked
                elif sponsor_button.collidepoint(event.pos):
                    open_sponsor_page()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    input_focus = "break" if input_focus == "work" else "work"
                elif event.key == pygame.K_BACKSPACE:
                    if input_focus == "work":
                        work_input = work_input[:-1]
                    else:
                        break_input = break_input[:-1]
                elif event.unicode.isdigit():
                    if input_focus == "work":
                        work_input += event.unicode
                    else:
                        break_input += event.unicode
        pygame.display.update()

def main():
    while True:
        if not on_timer_page:
            first_page()
        else:
            start_timer()

if __name__ == "__main__":
    main()

