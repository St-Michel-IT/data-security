"""
A flask app that return the IBAN of the dummy bank Dulac.
"""
from flask import Flask

app = Flask(__name__)

# The IBAN of St-Michel bank account
IBAN = "FR89 2004 1010 0505 0001 3M02 606"


@app.route('/iban/')
def iban():
    """
    Returns the IBAN of St-Michel bank account.
    """
    return IBAN


if __name__ == '__main__':
    app.run(debug=True, port=5002)
