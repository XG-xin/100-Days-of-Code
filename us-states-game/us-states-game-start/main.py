import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pandas.read_csv("50_states.csv")
state_list = data.state.to_list()
turtle = turtle.Turtle()
turtle.hideturtle()
turtle.penup()


guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"Guess the State {len(guessed_states)}/50",
                                    prompt="What's another state's name?").title()
    if answer_state == "Exit":
        # states_to_learn = []
        # for state_name in state_list:
        #     if state_name not in guessed_states:
        #         states_to_learn.append(state_name)
        states_to_learn = [state_name for state_name in state_list if state_name not in guessed_states]
        df = pandas.DataFrame(states_to_learn)
        df.to_csv("states_too_learn.csv")
        break
    if answer_state in state_list:
        guessed_states.append(answer_state)
        position = data[data.state == answer_state]
        turtle.goto(int(position.x), int(position.y))
        turtle.write(answer_state, True, align="center")

# screen.exitonclick()
states_to_learn = [state_name for state_name in state_list if state_name not in guessed_states]