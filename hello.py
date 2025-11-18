# import Flask module
from flask import Flask, render_template, request
import os
import logging
from werkzeug.utils import secure_filename

# create Flask app instance (atur folder template ke 'views')
app = Flask(__name__, template_folder='views')

# folder untuk menyimpan file upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# define route for the root URL
# @app.route('/')
# def hello_world():
#     # render halaman utama menggunakan main.html dan kirimkan title
#     return render_template('main.html', title='Home')

# define route untuk about
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# define route untuk contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
       # proses data form di sini (gunakan .get agar aman ketika field tidak ada)
        name = request.form.get('name')
        email = request.form.get('email')
        pesan = request.form.get('pesan')

        #  Tampilkan pada terminal (jika ada)
        logging.info(f"Contact form submitted: name={name}, email={email}")

    title = "Contact Page"
    return render_template('contact.html', title=title)
  

@app.route('/pmb', methods=['GET', 'POST'])
def pmb():
    if request.method == 'POST':
        # proses data form di sini
        nama = request.form.get('nama')
        alamat = request.form.get('alamat')
        tempat_lahir = request.form.get('tempat_lahir')
        tanggal_lahir = request.form.get('tanggal_lahir')
        asal_sma = request.form.get('asal_sma')
        jurusan = request.form.get('jurusan')

        foto = request.files.get('foto')
        foto_filename = None
        error = None
        if foto and foto.filename:
            try:
                filename = secure_filename(foto.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(save_path)
                foto_filename = filename
            except Exception as e:
                logging.exception('Failed to save uploaded foto')
                error = 'Gagal menyimpan foto. Coba lagi.'

        #  Tampilkan ringkasan di terminal (atau simpan ke DB)
        logging.info(f"PMB submission: nama={nama}, alamat={alamat}, tempat_lahir={tempat_lahir}, tanggal_lahir={tanggal_lahir}, asal_sma={asal_sma}, jurusan={jurusan}, foto={foto_filename}")

        if error:
            return render_template('pmb.html', title='PMB', error=error)
        return render_template('pmb.html', title='PMB', success=True)

    # juga layani /home ke halaman utama
    return render_template('pmb.html', title='PMB')

@app.route('/')
def home():
    # juga layani /home ke halaman utama
    return render_template('home.html', title='Home') 

# run the app
if __name__ == '__main__':
    app.run(debug=True)
