from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def init_db():
    with sqlite3.connect('contact.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS contacts
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         email TEXT NOT NULL,
                         message TEXT NOT NULL);''')
        conn.commit()

# Route to show the contact form
@app.route('/')
def index():
    return render_template('contact_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Save the data to SQLite database
        with sqlite3.connect('contact.db') as conn:
            conn.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', 
                         (name, email, message))
            conn.commit()
        
        return redirect(url_for('thank_you'))

# Route to show thank you page after submission
@app.route('/thank-you')
def thank_you():
    return '<h1>Thank you for contacting us!</h1>'

if __name__ == '__main__':
    init_db()  # Initialize database
    app.run(debug=True)