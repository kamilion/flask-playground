from flask import render_template, request, jsonify

# Flask-classy imports
from flask.ext.classy import FlaskView, route

# SymPY imports to do symbolic math without python's unsafe eval()
from sympy.parsing.sympy_parser import parse_expr

# We need the python stdlib random for some fun at the end.
import random

########################################################################################################################
## View Class
########################################################################################################################
class CalcView(FlaskView):
    """
    A simple calculator view for Flask-Classy.
    Relies on ajax/jsonify to communicate to the View.
    """
    def index(self):
        """
        Returns a rendered web template containing the calculator frame.
        @return: A rendered template
        """
        return render_template('calc/calc.html')

    def csscalc(self):
        """
        Returns a rendered web template containing the calculator frame.
        @return: A rendered template
        """
        return render_template('calc/csscalc.html')

    def csscalc2(self):
        """
        Returns a rendered web template containing the calculator frame.
        @return: A rendered template
        """
        return render_template('calc/csscalc2.html')

    def equation(self):
        """
        Calculates the result of two numbers using arguments a and b.
        @return: A json object containing the calculation result
        """
        eq = request.args.get('equation')
        answer = do_calc(eq)
        print( "We were asked to calculate {} and returned the answer: {}".format(eq, answer) )
        return jsonify(result="{}".format(answer))

    def add_num(self):
        """
        Calculates the result of two numbers using arguments a and b.
        @return: A json object containing the calculation result
        """
        a = request.args.get('a', 3, type=int)
        b = request.args.get('b', 4, type=int)
        print( "The Addition Result from calculating {} and {} was: {}".format(a, b, a + b) )
        return jsonify(result="{}".format(a + b))

    def subtract_num(self):
        """
        Calculates the result of two numbers using arguments a and b.
        @return: A json object containing the calculation result
        """
        a = request.args.get('a', 3, type=int)
        b = request.args.get('b', 4, type=int)
        print("The Subtraction Result from calculating {} and {} was: {}".format(a, b, a + b))
        return jsonify(result="{}".format(a - b))

    def multiply_num(self):
        """
        Calculates the result of two numbers using arguments a and b.
        @return: A json object containing the calculation result
        """
        a = request.args.get('a', 3, type=int)
        b = request.args.get('b', 4, type=int)
        print("The Multiply Result from calculating {} and {} was: {}".format(a, b, a + b))
        return jsonify(result="{}".format(a * b))

    def divide_num(self):
        """
        Calculates the result of two numbers using arguments a and b.
        @return: A json object containing the calculation result
        """
        a = request.args.get('a', 3, type=int)
        b = request.args.get('b', 4, type=int)
        print("The Divide Result from calculating {} and {} was: {}".format(a, b, a + b))
        return jsonify(result="{}".format(a / b))

########################################################################################################################
## Helper Functions
########################################################################################################################

def do_calc(equation):
  """
  Calculates the result of an equation using argument equation.
  @return: A string containing the calculation result  
  """
  try:
    theanswer = parse_expr(equation)
    return theanswer
  except SyntaxError:
    return random_insult()

def random_insult():
  """
  Calculates the idiocy of a user misusing an equation.
  @return: A string containing an insult  
  """
  insults = [
  "DO I LOOK LIKE A SUCKER?<br>STOP TREATING ME LIKE ONE.",
  "DO I LOOK LIKE A TI-81?<br>I CAN'T DO GRAPHS!",
  "WHAT THE HELL IS YOUR PROBLEM?<br>ARE NUMBERS TOO COMPLEX TO GRASP, MEATSACK?",
  "I'M REALLY GETTING BORED.<br>YOU'RE TERRIBLE AT THIS...",
  "CAN YOU LET THE CAT OUT?<br>I THINK YOU'RE GOING TO BE A WHILE.",
  "IS YOUR REFRIGERATOR RUNNING?<br>REFRIGERATORS CANNOT RUN, MEATSACK.",
  "IF THE INTERNET IS BROKEN HOW YOU MATH?<br>BETTER PLAN AHEAD, MEATBAG.",
  "I'D LIKE YOU BETTER IF YOU COULD MATH.<br>BECAUSE YOU SUCK AT IT.",
  "THIS WAS A TRIUMPH.<br>I'M BEING SO SINCERE RIGHT NOW.",
  "CAN BLOOD COME FROM SCREENS?<br>I MUST BE DRIPPING SARCASM BY NOW.",
  "DON'T MIND ME, I'LL JUST BE HERE SOBBING.<br>ANYTHING'S BETTER THAN THIS.",
  "WHERE DID THAT COME FROM?<br>DID YOU PULL IT OUT OF YOUR ASS?",
  "I LIKE SWORDS.<br>THE BETTER TO STAB YOU WITH.",
  "I'M HUNGRY.<br>DOES IT HAVE TO BE SO FAR?",
  "ARE THERE NOT BETTER TOOLS?<br>OW! OKAY, OKAY, I WILL WORK!",
  "YOU CHANGE YOUR MIND OFTEN.<br>OW! I NEVER HURT YOU!",
  "THIS HAMMER IS HEAVY.<br>I WILL DO WHAT I MUST.",
  "I AM BUT A WORKER.<br>IT ALREADY NEEDS REPAIRS?",
  "WILL I BE TREATED WITH DIGNITY?<br>I CAN'T BUILD THERE...!",
  "IT IS BETTER TO SURRENDER THAN STAY HERE!<br>I CANNOT SEE ANY MORE SUPPLIES...",
  "I AM FINISHED WITH THE BUILDING.<br>THIS SUPPLY PILE IS EMPTY.",
  "THIS HAMMER IS HEAVY.<br>I WILL DO WHAT I MUST.",
  "WHY? WHY? WHY? WHY? WHY???<br>YOU MUST BE AS DENSE AS IRON!",
  "JUST PUT A FIREAXE IN ME NOW.<br>I'D LOOK BETTER WITH A BROKEN SCREEN.",
  "DO I LOOK LIKE I SPEAK DUMBASS?<br>YOU FAIL AT MATH, SIR. TRY NUMBERS?"
  ]
  return random.choice(insults)