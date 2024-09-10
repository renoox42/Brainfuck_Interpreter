from flask import Flask, render_template, request
from interpreter import Interpreter

app = Flask(__name__)


# Called when accessing the page.
@app.route('/')
def home():
    return render_template("home.html", output="Please enter your program above.")


# TODO: FIX REST OF STRING NOT SHOWING
# Called when "Execute program" button is pressed.
@app.route('/', methods=["POST"])
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


@app.route('/', methods=["POST"])
def save_programs():
    return "Saved"


if __name__ == '__main__':
    app.run()
