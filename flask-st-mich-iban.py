"""
A flask app that return the IBAN of St-Michel bank account.
"""
from flask import Flask

app = Flask(__name__)

# The IBAN of St-Michel bank account
IBAN = "FR76 3000 6000 0112 3456 7890 189"


@app.route('/iban/')
def iban():
    """
    Returns the IBAN of St-Michel bank account.
    """
    return IBAN


if __name__ == '__main__':
    app.run(debug=True, port=5001)
