from flask import Flask, render_template, request
from interpreter import Interpreter
import sqlite3

app = Flask(__name__)


# Called when accessing the page.
@app.route('/')
def home():
    return render_template("home.html", output="Please enter your program above.")


# TODO: FIX REST OF STRING NOT SHOWING
# Called when "Execute program" button is pressed.
@app.route('/execute_request', methods=["POST"])
def execute_request():
    # Button for saving was pressed
    if request.form["buttons"] == "save":
        return save_program()

    # Button for executing was pressed
    user_input = request.form["user_input"]
    edited_input = (user_input.replace("\n", "")
                    .replace(" ", "").replace("\r", "").strip())

    if request.form["max_instructions"] == "":
        return render_template("home.html", output=f"> Error. No instruction limit given. <",
                               max_instructions=request.form["max_instructions"], user_input=user_input,
                               program_input=request.form["program_input"],
                               output_color="#990000")

    interpreter = Interpreter()
    interpreter_return_value = interpreter.interpret(edited_input, (int(request.form["max_instructions"])),
                                                     request.form["program_input"])

    error_code = interpreter_return_value[1]
    if error_code == 0:
        color = "black"
    elif error_code == 1:
        # red
        color = "#990000"
    else:
        # orange
        color = "#dd6800"

    result = interpreter_return_value[0]
    return render_template("home.html", output=f"> {result} <",
                           max_instructions=request.form["max_instructions"],
                           user_input=user_input, program_input=request.form["program_input"],
                           output_color=color)


def save_program():
    name = request.form["username"].strip()
    user_input = request.form["user_input"]
    edited_input = (user_input.replace("\n", "")
                    .replace(" ", "").replace("\r", "").strip())

    error = None
    if edited_input == "":
        error = "Not saved. No program entered."

    if not valid_chars(edited_input):
        error = "Not saved. Invalid characters in program."

    if name == "":
        error = "Not saved. No username entered."

    if error is not None:
        return render_template("home.html", output=f"> {error} <",
                               max_instructions=request.form["max_instructions"],
                               user_input=user_input, program_input=request.form["program_input"],
                               output_color="#990000")

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO programs (username, program) VALUES (?, ?)",
                   (name, edited_input))
    connection.commit()

    return render_template("home.html", output=f"> Saved program. <",
                           max_instructions=request.form["max_instructions"],
                           user_input=user_input, program_input=request.form["program_input"],
                           output_color="black")


def valid_chars(program: str):
    for i in range(0, len(program)):
        c = program[i]
        if c != '<' and c != ">" and c != "+" and c != "-" and c != "." and c != "," and c != "[" and c != "]":
            return False
    return True


if __name__ == '__main__':
    app.run()
