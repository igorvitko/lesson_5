from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, request

app = Flask("__main__")

key = Fernet.generate_key()

@app.route('/')
def start():
    """
    The main page with navigation

    """
    return "<h2>Start Lesson_5</h2> </hr><p><a href='/encrypt'>Зашифровать текст</a><br>" \
           "<a href='/decrypt'>Расшифровать токен</a></p>"


@app.route('/encrypt', methods=('GET', 'POST'))
def encrypt():
    """
    Encrypting entered string

    :return:
    A page with ciphertext that cannot be read or altered without the <key>.
    The format of page is, for example - "Encrypted result: adf9420-12fnkadl;f=4fjmqe"
    """

    string = request.args.get('string', None)

    if string is None and request.method == 'GET':
        return "<form method = 'POST'> <p>Введите текст</p> <p><input name='string'>" \
                   "<input type='submit' text='Подтвердить'></p></form>"

    if request.method == 'POST':
        string = request.form['string']

    if not string:
        return "<form method = 'POST'> <p>Введите текст</p> <p><input name='string'>" \
                   "<input type='submit' text='Подтвердить'></p></form>"\
               "<p><i>Attention!<br>Please enter text</i></p>"

    result = Fernet(key).encrypt(bytes(string, encoding='utf-8')).decode(encoding='utf-8')
    params = {
        'text': "Encrypted result:",
        'result': result,
         }
    return render_template('index.html', **params)


@app.route("/decrypt", methods=('GET', 'POST'))
def decrypt():
    """
    Decrypting entered string
    If entered incorrect token will be raise Exception

    :return:
    The page with original plaintext.
    The format of page is, for example - "Decrypted result: Hello World!"
    """

    string = request.args.get('string', None)

    if string is None and request.method == "GET":

        return "<form method = 'POST'> <p>Введите токен</p> <p><input name='string'>" \
               "<input type='submit' text='Подтвердить'></p></form>"

    if request.method == 'POST':
        string = request.form['string']

    try:
        result = Fernet(key).decrypt(bytes(string, encoding='utf-8')).decode()
    except InvalidToken:
        return "<form method = 'POST'> <p>Введите токен</p> <p><input name='string'>" \
               "<input type='submit' text='Подтвердить'></p></form>" \
               "<p><b>Error!</b><br><i>Don't Panic! Enter correct token</i></p>"

    params = {
        'text': "Decrypted result:",
        'result': result,
    }

    return render_template('index.html', **params)



if __name__ == '__main__':
    app.run(debug=True)