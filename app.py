from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from handlerPdf import cutterPDF

app = Flask(__name__)

BASE_DIR = 'download/'

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

@app.route('/', methods=['GET' , 'POST'])
def upload_file():
    if request.method == 'POST':
        email = request.form['email']
        file_name = request.form['file_name']
        makePdf = cutterPDF(os.path.join(BASE_DIR, file_name),email).action()
    return render_template('upload.html')

@app.route('/result', methods=['POST'])
def send_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file_obj = request.files.getlist("file")
    file_name = ""
    for file in file_obj:
        file_name = secure_filename(file.filename)
        file.save(os.path.join(BASE_DIR, file_name))
    try:
        return render_template('success.html', file_name=file_name)
    except:
        return render_template('error.html')

def start():
    if __name__ == '__main__':
        port = int(os.getenv('PORT', 8000))
        print("Starting app on port %d" % port)
        app.run(debug=False, port=port, host='0.0.0.0')

start()
