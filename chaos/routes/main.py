from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required, logout_user 

from chaos.extensions import db
from chaos.models import User 
from datetime import datetime 
import pytz
import os 
import requests 

main = Blueprint('main',__name__)

def get_cnt_n_hints_for(question_number):
    # write all hints and answers here

    hints = [
            [("Hint", "Read the Quote again"), 
            ("Hint", "Focus on words 'reverse' and 'language' "), 
            ("Hint", "Reverse the code word"), 
            ("Answer", "welcome (Explanation: Time cannot be reversed, who said language cannot be?!! the given  string is the reversed format of 'herzlich wilkommen' , welcome in German)")],

            [("Hint", "Google Googol"), 
            ("Hint", "log(100) = 2, 2 is the value that 10 must be raised to, to get 100"), 
            ("Hint", "modulo division gives the remainder after division (Example: 5 % 2 = 1)"), 
            ("Answer", "98 (Explanation: Googol is 1 followed by a hundred zeros. Google was founded in 1998. Modulo division is the remainder obtained after a division. Thus 1998 \% \log(Googol) = 98)")],


            [("Hint", "If I come to your house, it won't be a pleasant day for you"), 
            ("Hint", "An anagram is a word or phrase formed by rearranging the letters of a different word or phrase"), 
            ("Hint", "I'm so famous rather infamous now a days that I come on the news everywhere and everyday"), 
            ("Answer", "coronavirus (Explanation: 'coronavirus' is an anagram of 'carnivorous'. Seems trendy enough?)")],
            
            
            [("Hint", "Remember the language used in first question"), 
            ("Hint", "This city was divided into East and West till 1990"), 
            ("Hint", "A character in Money Heist"), 
            ("Answer", "Berlin (Explanation: JFK in his famous speech in Berlin Germany, infamously said 'Ich bin ein Berliner' which translates to 'I am a jelly dougnut', the city here refers to Berlin.)")],


            [("Hint", "Sometimes all you can do is write down what you see"), 
            ("Hint", "Yeah it is Morse code!"), 
            ("Hint", " Go to https://morsecode.world/international/translator.html"), 
            ("Answer", "enilsihtesrever (Explanation:  every dah is '-' and every dit is a '.' The given series is a morse code pattern that says 'reversethisline'. So you have to do just that!!)")],
            
            
            [("Hint", "It’s not arithmetic"), 
            ("Hint", "You know right, all places in the world can be virtualized, Search there to get the answer"), 
            ("Hint", "I symbolize love"), 
            ("Answer", "heart (Explanation: The above two numbers are the coordinates of the globe. Entering them in google maps will lead you to a 'heart'.)")],

            [("Hint", "I am a Nobel prize winning physicist"), 
            ("Hint", "My cat is very popular"), 
            ("Hint", "Search in special temporary alteration of logo on the world's famous search engine"), 
            ("Answer", "Schrodinger (Explanation: clicking the 'Im feeling lucky' button in google.com leads to doodles. The only doodle that was featured on that day was of Schrödinger's!)")],

            [("Hint", "Concentrate ?"), 
            ("Hint","I become curious when I see something blinking on my screen, won't you…??",), 
            ("Hint", "How much did you earn from '?' "), 
            ("Answer","200 (Explanation: Google has this Easter egg in the search page of Super Mario Bros. Clicking on the blinking box, you score '200' !!)")],

            [("Hint", "Some say everything humans know today can be found in this world"), 
            ("Hint", "Just use the link below; if you have missed it"), 
            ("Hint", "Its Greek letter that represents angular velocity"), 
            ("Answer", "omega (Explanation: Wikipedia logo is the world of puzzles! The only Greek alphabet on it is 'omega' !)")],

            [("Hint", "Some versions of it glow"), 
            ("Hint", "The key-word to decrypt is related to electronics"), 
            ("Hint", "focus on 'one way', 'rectify' and 'biased' in the riddle, don't forget to 'decode'"), 
            ("Answer", "Chaos is a ladder (Explanation: A simple diode(keyword) lets current flow in 'one way' that is when it is forward 'biased', this property is used in 'rectifiers' to convert 'oscillating' AC to DC)")],

            [("Hint", "Search a bit about the enigma machine. use '?' in the emulator to know more"), 
            ("Hint", "Make sure you make the proper connections!"), 
            ("Hint", "This is a secret society having an eye on a pyramid"), 
            ("Answer", "ILLUMINATI (Explanation: In the the enigma decryptor given, by setting the initial rotor positions as N I E, and connecting M-Y, S-O, R-E connections and typing KUANPVEMLX, would give 'illuminati')")],

            [("Hint", "Observe carefully"), 
            ("Hint", "Always try to 'know more' "), 
            ("Hint", "There are no errors in this game"), 
            ("Answer", "not available (Explanation: The point is to never give up! Click to know more page leads to another page where the answer is 'not available'. :P)")],

            [("Hint", "Browse this library according to the rules, don't forget the hex!"), 
            ("Hint", "If you have found a sentence, its actually a question"), 
            ("Hint", "Answer might surprise you, it's a number"), 
            ("Answer", "42 (Explanation: You should have figured out how to 'browse' the library, but the answer for that sentence is calculated by a supercomputer in 'The Hitchhiker's Guide to the Galaxy', and its 42. Interesting right.)")],

            [("Hint", "Expansion of pi: 3.141592653589793238462643383279502884197169"), 
            ("Hint", "The no. you are searching in pi lies between 500 - 700"), 
            ("Hint", "ISBN: International Standard Book Number, Usually found in the reference section"), 
            ("Answer", "05214-8455-3 (Explanation: The first 3 consecutive digits that's prime in PI are 653. Replacing x with 653 in the link, would lead to a page where a number is followed after ISBN '05214-8455-3'. That's the answer!!)")],

            [("Hint", "Read the riddle carefully and find out what the 'thing' is or rather its name"), 
            ("Hint", "If you have got the password, and found out the other clue, YOU should be able to solve this"), 
            ("Hint", "And its not the word 'you'! its you"), 
            ("Answer", "{} (Explanation: yeah its your username)".format(current_user.name))]
    
    ]

    return (2, hints[question_number - 1])

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/instructions')
@login_required
def instructions():
    return render_template('inst.html', user=current_user)

@main.route('/disp_question')
@login_required
def disp_question():
    if current_user.nextq == 16:
        return redirect(url_for('main.treasure'))
    for i in range(1, 16):
        if current_user.nextq == i:
            return redirect(url_for('main.q' + str(i)))

@main.route('/illuminati')
def illuminati():
    return render_template('illuminati.html')


@main.route('/treasure')
@login_required
def treasure():
    return render_template('treasure.html')

@main.route('/finish')
@login_required
def finish():
    return render_template('finish.html')

@main.route('/OEYQ====', methods=['GET', 'POST'])
@login_required
def q1():
    if current_user.nextq != 1:
        return redirect(url_for('main.disp_question'))
    return render_template('q1.html')   

@main.route('/OEZA====', methods=['GET', 'POST'])
@login_required
def q2():
    if current_user.nextq != 2:
        return redirect(url_for('main.disp_question'))
    return render_template('q2.html') 


@main.route('/OEZQ====', methods=['GET', 'POST'])
@login_required
def q3():
    if current_user.nextq != 3:
        return redirect(url_for('main.disp_question'))
    return render_template('q3.html') 


@main.route('/MNXXE4TFMN2A====', methods=['GET', 'POST'])
@login_required
def correct():
    return render_template('correct.html')

@main.route('/OE2A====', methods=['GET', 'POST'])
@login_required
def q4():
    if current_user.nextq != 4:
        return redirect(url_for('main.disp_question'))
    return render_template('q4.html') 

@main.route('/OE2Q====', methods=['GET', 'POST'])
@login_required
def q5():
    if current_user.nextq != 5:
        return redirect(url_for('main.disp_question'))
    return render_template('q5.html') 

@main.route('/OE2B====', methods=['GET', 'POST'])
@login_required
def q6():
    if current_user.nextq != 6:
        return redirect(url_for('main.disp_question'))
    return render_template('q6.html')

@main.route('/OE2X====', methods=['GET', 'POST'])
@login_required
def q7():
    if current_user.nextq != 7:
        return redirect(url_for('main.disp_question'))
    return render_template('q7.html')

@main.route('/OE3X====', methods=['GET', 'POST'])
@login_required
def q8():
    if current_user.nextq != 8:
        return redirect(url_for('main.disp_question'))
    return render_template('q8.html')

@main.route('/OE4G====', methods=['GET', 'POST'])
@login_required
def q9():
    if current_user.nextq != 9:
        return redirect(url_for('main.disp_question'))
    return render_template('q9.html')

@main.route('/OE5C====', methods=['GET', 'POST'])
@login_required
def q10():
    if current_user.nextq != 10:
        return redirect(url_for('main.disp_question'))
    return render_template('q10.html')

@main.route('/OE5E====', methods=['GET', 'POST'])
@login_required
def q11():
    if current_user.nextq != 11:
        return redirect(url_for('main.disp_question'))
    return render_template('q11.html')

@main.route('/OE7X====', methods=['GET', 'POST'])
@login_required
def q12():
    if current_user.nextq != 12:
        return redirect(url_for('main.disp_question'))
    return render_template('q12.html')

@main.route('/OEYTG===', methods=['GET', 'POST'])
@login_required
def q13():
    if current_user.nextq != 13:
        return redirect(url_for('main.disp_question'))
    return render_template('q13.html') 

@main.route('/OEYTI===', methods=['GET', 'POST'])
@login_required
def q14():
    if current_user.nextq != 14:
        return redirect(url_for('main.disp_question'))
    return render_template('q14.html')

@main.route('/OEYTK===', methods=['GET', 'POST'])
@login_required
def q15():
    if current_user.nextq != 15:
        return redirect(url_for('main.disp_question'))
    return render_template('q15.html')

@main.route('/treasurehuntv1.0', methods=['GET', 'POST'])
@login_required
def error1():
    return render_template('errorpage.html')

@main.route('/404', methods=['GET', 'POST'])
@login_required
def error2():
    return render_template('errorpageanswer.html') 


@main.route('/pro1', methods=['GET','POST'])
@login_required
def pro1():
    if current_user.nextq != 1:
        logout_user()
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(1)
        at = str(current_user.attempts)
        score = int(current_user.score)
        if request.form['Answer'].lower().strip() == "welcome":
            if current_user.hint == -1:
                score += 20
                at += '1,20| '
            elif current_user.hint == 0:
                score += 15
                at += '1,15| '
            elif current_user.hint == 1:
                score += 10
                at += '1,10| '
            elif current_user.hint == 2:
                score += 5
                at += '1,5| '
            elif current_user.hint == 3:
                at += '1,0| '

            current_user.attempts = at 
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try < max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q1'))

    return redirect(url_for('main.q1'))

@main.route('/pro2', methods=['GET','POST'])
@login_required
def pro2():
    if current_user.nextq != 2:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(2)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip() == "98":
            if current_user.hint == -1:
                score += 20
                at += '2,20| '
            elif current_user.hint == 0:
                score += 15
                at += '2,15| '
            elif current_user.hint == 1:
                score += 10
                at += '2,10| '
            elif current_user.hint == 2:
                score += 5
                at += '2,5| '
            elif current_user.hint == 3:
                at += '2,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q2'))

    return redirect(url_for('main.q2'))



@main.route('/pro3', methods=['GET','POST'])
@login_required
def pro3():
    if current_user.nextq != 3:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(3)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="coronavirus":
            if current_user.hint == -1:
                score += 20
                at += '3,20| '
            elif current_user.hint == 0:
                score += 15
                at += '3,15| '
            elif current_user.hint == 1:
                score += 10
                at += '3,10| '
            elif current_user.hint == 2:
                score += 5
                at += '3,5| '
            elif current_user.hint == 3:
                at += '3,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q3'))

    return redirect(url_for('main.q3'))

@main.route('/pro4', methods=['GET','POST'])
@login_required
def pro4():
    if current_user.nextq != 4:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(4)
        at = str(current_user.attempts)
        score = int(current_user.score)
        if request.form['Answer'].lower().strip()=="berlin":
            if current_user.hint == -1:
                score += 20
                at += '4,20| '
            elif current_user.hint == 0:
                score += 15
                at += '4,15| '
            elif current_user.hint == 1:
                score += 10
                at += '4,10| '
            elif current_user.hint == 2:
                score += 5
                at += '4,5| '
            elif current_user.hint == 3:
                at += '4,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q4'))

    return redirect(url_for('main.q4'))

@main.route('/pro5', methods=['GET','POST'])
@login_required
def pro5():
    if current_user.nextq != 5:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(5)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="enilsihtesrever":
            if current_user.hint == -1:
                score += 20
                at += '5,20| '
            elif current_user.hint == 0:
                score += 15
                at += '5,15| '
            elif current_user.hint == 1:
                score += 10
                at += '5,10| '
            elif current_user.hint == 2:
                score += 5
                at += '5,5| '
            elif current_user.hint == 3:
                at += '5,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q5'))

    return redirect(url_for('main.q5'))

@main.route('/pro6', methods=['GET','POST'])
@login_required
def pro6():
    if current_user.nextq != 6:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(6)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="heart":
            if current_user.hint == -1:
                score += 20
                at += '6,20| '
            elif current_user.hint == 0:
                score += 15
                at += '6,15| '
            elif current_user.hint == 1:
                score += 10
                at += '6,10| '
            elif current_user.hint == 2:
                score += 5
                at += '6,5| '
            elif current_user.hint == 3:
                at += '6,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q6'))

    return redirect(url_for('main.q6'))

@main.route('/pro7', methods=['GET','POST'])
@login_required
def pro7():
    if current_user.nextq != 7:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(7)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="erwin schrödinger" or request.form['Answer'].lower().strip()=="schrödinger" or request.form['Answer'].lower().strip()=="erwin schrodinger" or request.form['Answer'].lower().strip()=="schrodinger" :
            if current_user.hint == -1:
                score += 20
                at += '7,20| '
            elif current_user.hint == 0:
                score += 15
                at += '7,15| '
            elif current_user.hint == 1:
                score += 10
                at += '7,10| '
            elif current_user.hint == 2:
                score += 5
                at += '7,5| '
            elif current_user.hint == 3:
                at += '7,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q7'))

    return redirect(url_for('main.q7'))

@main.route('/pro8', methods=['GET','POST'])
@login_required
def pro8():
    if current_user.nextq != 8:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(8)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip() == '200':
            if current_user.hint == -1:
                score += 20
                at += '8,20| '
            elif current_user.hint == 0:
                score += 15
                at += '8,15| '
            elif current_user.hint == 1:
                score += 10
                at += '8,10| '
            elif current_user.hint == 2:
                score += 5
                at += '8,5| '
            elif current_user.hint == 3:
                at += '8,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q8'))

    return redirect(url_for('main.q8'))

@main.route('/pro9', methods=['GET','POST'])
@login_required
def pro9():
    if current_user.nextq != 9:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(9)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="omega":
            if current_user.hint == -1:
                score += 20
                at += '9,20| '
            elif current_user.hint == 0:
                score += 15
                at += '9,15| '
            elif current_user.hint == 1:
                score += 10
                at += '9,10| '
            elif current_user.hint == 2:
                score += 5
                at += '9,5| '
            elif current_user.hint == 3:
                at += '9,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q9'))

    return redirect(url_for('main.q9'))


@main.route('/pro10', methods=['GET','POST'])
@login_required
def pro10():
    if current_user.nextq != 10:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(10)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="chaos is a ladder" :
            if current_user.hint == -1:
                score += 20
                at += '10,20| '
            elif current_user.hint == 0:
                score += 15
                at += '10,15| '
            elif current_user.hint == 1:
                score += 10
                at += '10,10| '
            elif current_user.hint == 2:
                score += 5
                at += '10,5| '
            elif current_user.hint == 3:
                at += '10,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q10'))

    return redirect(url_for('main.q10'))


@main.route('/pro11', methods=['GET','POST'])
@login_required
def pro11():
    if current_user.nextq != 11:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(11)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="illuminati" :
            if current_user.hint == -1:
                score += 20
                at += '11,20| '
            elif current_user.hint == 0:
                score += 15
                at += '11,15| '
            elif current_user.hint == 1:
                score += 10
                at += '11,10| '
            elif current_user.hint == 2:
                score += 5
                at += '11,5| '
            elif current_user.hint == 3:
                at += '11,0| '

            current_user.attempts = at

            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q11'))

    return redirect(url_for('main.q11'))

@main.route('/pro12', methods=['GET','POST'])
@login_required
def pro12():
    if current_user.nextq != 12:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(12)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="not available" :
            if current_user.hint == -1:
                score += 20
                at += '12,20| '
            elif current_user.hint == 0:
                score += 15
                at += '12,15| '
            elif current_user.hint == 1:
                score += 10
                at += '12,10| '
            elif current_user.hint == 2:
                score += 5
                at += '12,5| '
            elif current_user.hint == 3:
                at += '12,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q12'))

    return redirect(url_for('main.q12'))


@main.route('/pro13', methods=['GET','POST'])
@login_required
def pro13():
    if current_user.nextq != 13:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(13)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="42" :
            if current_user.hint == -1:
                score += 20
                at += '13,20| '
            elif current_user.hint == 0:
                score += 15
                at += '13,15| '
            elif current_user.hint == 1:
                score += 10
                at += '13,10| '
            elif current_user.hint == 2:
                score += 5
                at += '13,5| '
            elif current_user.hint == 3:
                at += '13,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q13'))

    return redirect(url_for('main.q13'))

@main.route('/pro14', methods=['GET','POST'])
@login_required
def pro14():
    if current_user.nextq != 14:
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(14)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip()=="05214-8455-3" or request.form['Answer'].lower().strip()=="0521484553" :
            if current_user.hint == -1:
                score += 20
                at += '14,20| '
            elif current_user.hint == 0:
                score += 15
                at += '14,15| '
            elif current_user.hint == 1:
                score += 10
                at += '14,10| '
            elif current_user.hint == 2:
                score += 5
                at += '14,5| '
            elif current_user.hint == 3:
                at += '14,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q14'))

    return redirect(url_for('main.q14'))

@main.route('/pro15', methods=['GET','POST'])
@login_required
def pro15():
    if current_user.nextq != 15:
        logout_user()
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        max_cnt, hints = get_cnt_n_hints_for(15)
        score = int(current_user.score)
        at = str(current_user.attempts)
        if request.form['Answer'].lower().strip() == current_user.name.lower().strip():
            if current_user.hint == -1:
                score += 20
                at += '15,20| '
            elif current_user.hint == 0:
                score += 15
                at += '15,15| '
            elif current_user.hint == 1:
                score += 10
                at += '15,10| '
            elif current_user.hint == 2:
                score += 5
                at += '15,5| '
            elif current_user.hint == 3:
                at += '15,0| '

            current_user.attempts = at
            current_user.score = score
            current_user.nextq += int(1)
            current_user.present_try = 0
            current_user.hint = -1
            db.session.commit()
            if current_user.end_time == None:
                dt = datetime.now(tz=pytz.UTC)           
                current_user.end_time = dt.astimezone(pytz.timezone('Asia/Kolkata'))
                db.session.commit()
            return redirect(url_for('main.disp_question'))
            flash('')
        elif current_user.present_try <= max_cnt:
            current_user.present_try += int(1)
            db.session.commit()
            flash("You are wrong!! Try again.", "info") 
        else:
            if current_user.hint < 3:
                current_user.hint += 1
                db.session.commit()
                flash(f"{hints[current_user.hint][0]} : {hints[current_user.hint][1]}", "message")

        return redirect(url_for('main.q15'))

    return redirect(url_for('main.q15'))
