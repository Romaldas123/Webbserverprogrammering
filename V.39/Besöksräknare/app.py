from flask import Flask
import os

app = Flask(__name__)

FILE_PATH = os.path.join(os.path.dirname(__file__), "counter.txt")

@app.route("/")
def show_nbr_visitors():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            number = int(f.read().strip())  # .strip() tar bort radbrytningar
            number = number + 1
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(str(number))
    except Exception as e:
        return f"Fel vid filhantering: {e}"
    return f"Välkommen till sidan! Denna sida har laddats {str(number)} gånger."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
