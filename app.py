from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'mystical-secret-key'

with open('clues.json') as f:
    clues = json.load(f)

@app.route('/')
def index():
    return redirect(url_for('clue', clue_id=1))

@app.route('/clue/<int:clue_id>', methods=['GET', 'POST'])
def clue(clue_id):
    if 'name' not in session and clue_id != 1:
        return redirect(url_for('clue', clue_id=1))

    current_progress = session.get('progress', 1)
    if clue_id > current_progress:
        return "You haven't unlocked this clue yet!", 403

    clue = next((c for c in clues if c["id"] == clue_id), None)
    if not clue:
        return "Clue not found.", 404

    if request.method == 'POST':
        user_input = request.form.get('answer', '').strip().lower()

        if clue["type"] == "name":
            session['name'] = user_input
            session['progress'] = 2
            return render_template('clue.html', clue=clue, unlocked=True)

        elif user_input == clue["answer"]:
            session['progress'] = clue_id + 1
            if clue_id == len(clues):
                return redirect(url_for('complete'))
            return render_template('clue.html', clue=clue, unlocked=True)
        else:
            return render_template('clue.html', clue=clue, error="Hmm... that's not quite right.")

    return render_template('clue.html', clue=clue)

@app.route('/complete')
def complete():
    if session.get('progress', 1) < len(clues) + 1:
        return redirect(url_for('clue', clue_id=1))
    return render_template('complete.html')

if __name__ == '__main__':
    app.run(debug=True)
