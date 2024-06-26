# Intialize a Flask app and create a route that reads a file from the filesystem
from flask import Flask, send_from_directory, send_file, make_response, request
from os.path import abspath, join

app = Flask(__name__)


@app.route('/img-safe/<string:path>')
def img_safe(path):
    """
    As send_from_directory is used, it is safe to use this function.
     The function states "This is a secure way to serve files from a folder, such as static
    files or uploads. Uses :func:`~werkzeug.security.safe_join` to
    ensure the path coming from the client is not maliciously crafted to
    point outside the specified directory."

       :param path: Path of the image.
       :return: The image as a response.
    """
    # Works fine with http://127.0.0.1:5000/img-safe/ai-everywhere.png
    # But does not work with 127.0.0.1:5000/img-safe/../../../architecture-application/doc/image/monk-looking-the-deepness-of-the-stars-in-the-night-sky.png
    return send_from_directory("doc/image", path)


@app.route('/img-safe2/<string:path>')
def img_safe2(path):
    """
    This function is as well for the same reason as img_safe.

       :param path: Path of the image.
       :return: The image as a response.
    """
    return send_file(abspath(join("doc/image", path)))


@app.route('/img-unsafe/')
def img_unsafe():
    """
    Works with http://127.0.0.1:5000/img-unsafe/?path=../architecture-application/doc/image/monk-looking-the-deepness-of-the-stars-in-the-night-sky.png
    /etc/passwd
    """
    path = request.args.get("path")
    with open(path, 'rb') as f:
        response = make_response(f.read())
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.set(
            'Content-Disposition', 'attachment', filename='%s.jpg' % path.split('/')[-1])
        return response


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
