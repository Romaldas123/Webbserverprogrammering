from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Behövs för sessioner

PASSWORD = "Hello123"

# Exempeldata
adresser = {
    "Romaldas": "romaldas.blyza@skola.taby.se",
    "Mehran": "mehran.sediqi@skola.taby.se"
}

# Enkel HTML-mall för login
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Logga in</h2>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
    <form method="post">
        <label>Lösenord:</label>
        <input type="password" name="password">
        <input type="submit" value="Logga in">
    </form>
</body>
</html>
"""

@app.before_request
def require_login():
    if request.endpoint not in ("login", "static") and not session.get("logged_in"):
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            error = "Fel lösenord!"
    return render_template_string(login_page, error=error)

@app.route("/")
def home():
    return '''
        <p>Välkommen till Flask Routing! Du är inloggad ✅</p>
        <ul>
            <li><a href="/user/Romaldas">/user/[username]</a></li>
            <li><a href="/search?q=Romaldas">/search?q=[query]</a></li>
            <li><a href="/form">/form</a></li>
            <li><a href="/logout">Logga ut</a></li>
        </ul>
    '''

@app.route("/user/<username>")
def show_user_profile(username):
    return f'User: {username}'

@app.route("/search")
def search():
    query = request.args.get('q', '')
    if query in adresser:
        return f'Ditt namn är: {query}, din mailadress är: {adresser[query]}'
    return f'Ingen användare hittades med namnet {query}'

# GET route som visar ett enkelt formulär med textfält och checkbox
@app.route('/form')
def form():
    return '''
        <form action="/submit" method="post">
            <label for="data">Enter something:</label>
            <input type="text" id="data" name="data"><br>
            <input type="checkbox" id="checkbox" name="checkbox"><label for="checkbox">Check this</label> <br>
            <input type="submit" value="Submit">
        </form>
    '''

# POST route som hanterar formulärdata
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('data', '')  
    checkbox = request.form.get('checkbox', False)
    return f'Skickat via POST: {data}, Checkbox: {checkbox}'

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
