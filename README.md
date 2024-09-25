<h1>Brainfuck Interpreter Webapp</h1>
<p>This simple Webapp allows users to enter and execute their programs, save them to a database and manage their saved programs. <br>
Its backend uses the Flask web framework.
</p>
<h2>What is Brainfuck?</h2>
<p>
  Wikipedia: https://de.wikipedia.org/wiki/Brainfuck
</p>
<h2>Example Program</h2>
<p>
  This prints "Hello World!": <br>
  ++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.>+.+++++++..+++.<<++++++++++++++.------------.>+++++++++++++++.>.+++.------.--------.<<+.
</p>
<h2>Preview</h2>
<p>Home page view:</p>
<img width="630" alt="Bildschirmfoto 2024-09-25 um 18 33 12" src="https://github.com/user-attachments/assets/114ec0db-5a68-435e-81e8-352b616da4e5">
<p>Saved programs view:</p>
<img width="1230" alt="Bildschirmfoto 2024-09-25 um 18 33 55" src="https://github.com/user-attachments/assets/2e22331b-18b3-4966-84ad-bf5de7587da4">
<h2>How to run it?</h2>
<p>
  1. navigate to directory "brainfuck_interpreter" <br>
  2. run "python -m venv enviroment" <br>
  3. run "source environment/bin/activate" <br>
  4. run "pip install flask" <br>
  5. run "flask run" <br>
  <br>
  This creates a virtual environment to install flask on. Then the webapp is launched using flask. <br>
  Flask tells you on which address the webapp is running. Open this address in your browser of choice (on your machine).
</p>
