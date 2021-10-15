from turtle import Turtle, Screen
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
screen = Screen()
speed = 1000


class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.segments = []
        self.hideturtle()
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_cars(self):
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            new_segment = Turtle(shape="square")
            new_segment.penup()
            new_segment.shapesize(stretch_wid=1, stretch_len=2)
            new_segment.color(random.choice(COLORS))
            new_segment.goto(300, random.randint(-250, 250))
            self.segments.append(new_segment)

    def move(self):
        for seg_num in self.segments:
            seg_num.backward(self.car_speed)

    def increase_speed(self):
        self.car_speed += MOVE_INCREMENT
