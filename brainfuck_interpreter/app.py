from flask import Flask, render_template, request
from interpreter import Interpreter
import sqlite3

app = Flask(__name__)


# Called when accessing the page.
@app.route('/')
def home():
    return render_template("home.html", output="Please enter your program above.", output_color="green")


# TODO: FIX REST OF STRING NOT SHOWING
# TODO: REFACTORING
# Called when any button is pressed.
@app.route('/execute_request', methods=["POST"])
def execute_request():
    # Button for saving was pressed
    if request.form["buttons"] == "save":
        return save_program()
    # Button for viewing saved programs was pressed
    if request.form["buttons"] == "view":
        return view_programs(request.form["username"].strip(), request.form["user_input"])
    # Button for executing was pressed
    return execute_program()


def execute_program():
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


# Saves entered program to the database
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
    connection.close()

    return render_template("home.html", output=f"> Saved program. <",
                           max_instructions=request.form["max_instructions"],
                           user_input=user_input, program_input=request.form["program_input"],
                           output_color="green")


# Shows user his saved programs, if there are any.
def view_programs(name, user_input):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row
    programs = cursor.execute("SELECT * FROM programs WHERE username=?", (name,)).fetchall()
    connection.close()

    if len(programs) == 0:
        if user_input is None:
            return render_template("home.html", output=f"> Deleted {name}'s saved programs. <", output_color="green")
        return render_template("home.html", output=f"> No data for given username. <",
                               max_instructions=request.form["max_instructions"],
                               user_input=user_input, program_input=request.form["program_input"],
                               output_color="#990000")

    return render_template("saved_programs.html", programs=programs, name=name)


# Deletes every saved program of user and returns to main page
@app.route("/delete_history", methods=["POST"])
def delete_history():
    name = request.form["delete"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM programs WHERE username=?", (name,))
    connection.commit()
    connection.close()
    return render_template("home.html", output=f"> Deleted all of {name}'s saved programs. <", output_color="green")


# Deletes one specific program in user history
@app.route("/delete_one_program", methods=["POST"])
def delete_one_program():
    delete_id = int(request.form["delete_id"])

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    name = (cursor.execute("SELECT * FROM programs WHERE id=? LIMIT 1", (delete_id,)).fetchone())["username"]

    cursor.execute("DELETE FROM programs WHERE id=?", (delete_id,))
    connection.commit()
    connection.close()

    return view_programs(name, None)


# Checks if entered program contains only "brainfuck-valid" characters
def valid_chars(program: str):
    for i in range(0, len(program)):
        c = program[i]
        if c != '<' and c != ">" and c != "+" and c != "-" and c != "." and c != "," and c != "[" and c != "]":
            return False
    return True


if __name__ == '__main__':
    app.run()
