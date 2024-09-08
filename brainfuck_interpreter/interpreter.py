class Interpreter:
    """Class containing functionality of a brainfuck interpreter.

    Attributes
    ----------
    arr : bytearray
        Byte array of variable size where the instructions are executed on.
    """

    def __init__(self, size: int = 30000):
        """Constructor to initialize byte array.

        Parameters
        ----------
            size : int
                Size of byte array. Default size is 30000.
        """
        if size is None:
            self.arr = bytearray([0] * 30000)
        else:
            self.arr = bytearray([0] * size)

    def interpret(self, instructions, max_instructions, program_input):
        """Takes a string of instructions, an instruction limit and a program input and executes them on an empty
        byte array.

        Parameters
        ----------
            instructions : str
                The instructions to be executed.
            max_instructions : int
                Maximum number of instructions to be executed.
            program_input : str
                Input String read by the interpreter.
        Returns
        -------
            str, int
                The output string that results from executing the instructions and a corresponding error code.
                0 -> SUCCESS
                1 -> ERROR
                2 -> INSTRUCTION LIMIT EXCEEDED
        """
        error_message = "Error while processing the instructions."
        result = ""

        array_length = len(self.arr)
        program_length = len(instructions)
        program_pointer = 0
        array_pointer = 0
        program_index = 0
        counter = 1
        input_string_index = 0

        while True:
            # End of program reached
            if counter > max_instructions:
                return result + "<instruction limit exceeded>", 2

            if program_pointer >= program_length:
                return result, 0

            current_instruction = instructions[program_pointer]

            # Execute current instruction
            if current_instruction == ">":
                array_pointer += 1
                if array_pointer >= array_length:
                    return error_message, 1
            elif current_instruction == "<":
                array_pointer -= 1
                if array_pointer < 0:
                    return error_message, 1
            elif current_instruction == "+":
                increase = (self.arr[array_pointer] + 1) % 256
                self.arr[array_pointer] = increase
            elif current_instruction == "-":
                decrease = (self.arr[array_pointer] - 1) % 256
                self.arr[array_pointer] = decrease
            elif current_instruction == ".":
                result += chr(self.arr[array_pointer])
            elif current_instruction == ",":
                try:
                    char = program_input[input_string_index]
                    if char == "\\" and program_input[input_string_index + 1] == "0":
                        self.arr[array_pointer] = 0
                        input_string_index += 1
                    else:
                        self.arr[array_pointer] = ord(char)
                except IndexError:
                    return "Error. Not enough input given.", 1

                input_string_index += 1
            elif current_instruction == "[":
                if self.arr[array_pointer] == 0:
                    depth = 1
                    while True:
                        program_pointer += 1
                        program_index += 1

                        if program_index >= program_length:
                            return error_message, 1
                        if instructions[program_pointer] == "[":
                            depth += 1
                        elif instructions[program_pointer] == "]":
                            depth -= 1
                            if depth == 0:
                                break

                        if array_pointer >= array_length:
                            return error_message, 1
            elif current_instruction == "]":
                if self.arr[array_pointer] != 0:
                    depth = -1
                    while True:
                        program_pointer -= 1
                        program_index -= 1

                        if program_index < 0:
                            return error_message, 1

                        if instructions[program_pointer] == "[":
                            depth += 1
                            if depth == 0:
                                break
                        elif instructions[program_pointer] == "]":
                            depth -= 1

                        if array_pointer < 0:
                            return error_message, 1
            else:
                return error_message, 1

            program_index += 1
            program_pointer += 1
            counter += 1
