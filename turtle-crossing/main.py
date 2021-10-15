import time
from turtle import Screen
from player import Player
from car_manager import CarManager
import random
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()

screen.listen()
screen.onkey(player.move, "Up")

scoreboard = Scoreboard()
game_is_on = True

car = CarManager()

while game_is_on:
    time.sleep(0.1)
    screen.update()
    car.move()
    car.create_cars()
    # Detect successful crossing.
    if player.ycor() >= 290:
        scoreboard.add_score()
        player.game_rest()
        car.increase_speed()

    # Detect collision with car.
    for segment in car.segments:
        if segment.distance(player) < 20:
            scoreboard.game_over()
            game_is_on = False

screen.exitonclick()
