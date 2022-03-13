from curses import window
from operator import irshift
from flask import Flask, redirect, render_template, request, session
import random
app = Flask(__name__)
app.secret_key = "asdjhfpuiaheapsudihvpuw"

def generate_random_number():
    return random.randint(1,100)

#===========================================
# Main Index
#===========================================

#* ===========================================
#? Root Route  <==> RENDER FORM - /
#* ===========================================
@app.route('/')
def index():
    print(session)
    info_ret = {}
    if "user_guess" in session:
        info_ret["user_num"] = session['user_guess']
        info_ret["gen_num"] = session['generated_number']
        gen_numb = int(session['generated_number'])
        use_numb = int(session['user_guess'])
        if use_numb > gen_numb:
            info_ret["guess"] = "high"
        elif use_numb < gen_numb:
            info_ret["guess"] = "low"
        elif use_numb == gen_numb:
            info_ret["guess"] = "correct"
            session.pop('generated_number', None)
            session.pop('user_guess', None)
            session.pop('counter', None)
            session["finished"] = True
    print(session)
    if "counter" in session:
        info_ret["counter"] = session['counter']
    if "one_to_go" in session:
        info_ret["one_to_go"] = session['one_to_go']
    if "final_numb" in session:
        info_ret["final_numb_low"] = session['final_numb']
        
    
    return render_template("index.html", info_ret=info_ret)



#t- ===========================================
#? PROCESS FORM - /
#t- ===========================================
@app.route('/user_guess', methods=['POST']) 
def user_guess():
    print(session)
    if "finished" in session:
        if session["finished"]:
            return redirect("/reset")
        if "final_numb":
            return redirect("/")
    if "generated_number" in session:
         rnd_num = session["generated_number"]
    else:
        rnd_num = generate_random_number()
        session["generated_number"] = rnd_num
    if "counter" in session:
        session["counter"] += 1
        if session["counter"] == 9:
            session["one_to_go"] = True
        if session["counter"] >= 10:
            session["one_to_go"] = False
            session["final_numb"] = True
            session["finished"] = True
    else:
        session["counter"] = 1
    if request.form["user-guess"] != "":
        user_guess_input = int(request.form["user-guess"])
    else:
        user_guess_input = 0
    session["user_guess"] = user_guess_input
    return redirect("/")

@app.route("/play_again", methods=["POST"])
def play_again():
    print(session)
    return redirect("/reset")

@app.route("/reset")
def reset():
    session.clear()
    print(session)
    return redirect("/")



""" 

    info_ret = []
    if "generated_number" in session:
        info_ret.append({"gen_num" : session['generated_number']})
        print(f"Session generated_number: {session['generated_number']}")
    if "user_guess" in session:
        info_ret.append({"user_num" : session['user_guess']})
        print(f"Session user_guess {session['user_guess']}")
    if "counter" in session:
        info_ret.append({"counter" : session['counter']})
        print(f"Session'counter': {session['counter']}")
        
"""











#! MUST BE AT THE BOTTOM ---------------
if __name__ == "__main__":
    app.run(debug=True)
