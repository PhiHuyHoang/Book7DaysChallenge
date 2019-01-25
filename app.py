from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from handlerPdf import cutterPDF

app = Flask(__name__)

file_name = ""
base_dir = ""

@app.route('/', methods=['GET' , 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file_obj = request.files.getlist("file")
        file_name = ""
        try:
            for file in file_obj:
                file_name = secure_filename(file.filename)
                base_dir = file_name.replace(".pdf", "")
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir)
                file.save(os.path.join(base_dir, file_name))

                makePdf = cutterPDF(os.path.join(base_dir, file_name)).action()
                abs_path = os.path.join(base_dir)
                # Show directory contents
                files = os.listdir(abs_path)
                for f in files:
                    ext = os.path.splitext(f)[-1].lower()
                    print(ext)
                return render_template('success.html', files=files)
        except Exception as e:
            print(e)
            return render_template('error.html')
    return render_template('upload.html')


def start():
    if __name__ == '__main__':
        port = int(os.getenv('PORT', 8000))
        print("Starting app on port %d" % port)
        app.run(debug=False, port=port, host='0.0.0.0')

start()
