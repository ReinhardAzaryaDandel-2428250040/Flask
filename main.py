import pandas as pd  # Library untuk manipulasi data dalam bentuk DataFrame
import pickle  # Library untuk memuat model machine learning yang sudah disimpan
import logging
from flask import Flask, request, jsonify  # Flask untuk membuat web API, request untuk menerima data, jsonify untuk mengirim response JSON
from flask_cors import CORS  # Import Flask-CORS untuk mengizinkan akses dari domain berbeda (Cross-Origin Resource Sharing)

logging.basicConfig(level=logging.INFO)


# Membuat aplikasi Flask
app = Flask(__name__)


# Aktifkan CORS - Mengizinkan semua domain untuk mengakses API ini
# CORS diperlukan agar frontend (seperti website) dari domain lain bisa mengakses API ini
CORS(app)  # Mengizinkan semua domain


# Muat model yang sudah disimpan dari file model.pkl (jika ada)
try:
    with open('model.pkl', 'rb') as file:  # 'rb' = read binary
        model = pickle.load(file)
    logging.info('Loaded model from model.pkl')
except FileNotFoundError:
    model = None
    logging.warning('model.pkl not found - predictions will be unavailable until a model is provided')
except Exception:
    model = None
    logging.exception('Failed to load model.pkl')


# Muat scaler yang sudah disimpan untuk normalisasi data input (opsional)
try:
    with open('scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    logging.info('Loaded scaler from scaler.pkl')
except FileNotFoundError:
    scaler = None
    logging.warning('scaler.pkl not found - input will not be scaled')
except Exception:
    scaler = None
    logging.exception('Failed to load scaler.pkl')


# Endpoint untuk halaman home /
# Endpoint ini hanya menampilkan pesan selamat datang ketika user mengakses root URL
@app.route('/')
def welcome():
    return "<h1>Selamat Datang di API DS Model</h1>"


# Endpoint untuk memprediksi diabetes
# Endpoint ini menerima data pasien dan mengembalikan prediksi diabetes
@app.route('/predict', methods=['GET', 'POST'])
def predict_diabetes():
    # Jika GET: berikan petunjuk singkat agar pengguna tahu cara memakai endpoint
    if request.method == 'GET':
        return jsonify({
            'message': 'Send a POST request to this endpoint with JSON body containing the following keys: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age'
        })
    try:
        # Ambil data dari request body dalam format JSON
        # Data dikirim dari client (frontend/Postman) dalam format JSON
        data = request.get_json()


        # Buat DataFrame dengan nama kolom yang sesuai
        # DataFrame diperlukan karena model sklearn membutuhkan input dalam format DataFrame
        # Kolom-kolom ini harus sesuai dengan kolom yang digunakan saat training model
        input_data = pd.DataFrame([{
            "Pregnancies": data['Pregnancies'],  # Jumlah kehamilan
            "Glucose": data['Glucose'],  # Kadar glukosa dalam darah
            "BloodPressure": data['BloodPressure'],  # Tekanan darah
            "SkinThickness": data['SkinThickness'],  # Ketebalan kulit
            "Insulin": data['Insulin'],  # Kadar insulin
            "BMI": data['BMI'],  # Body Mass Index (indeks massa tubuh)
            "DiabetesPedigreeFunction": data['DiabetesPedigreeFunction'],  # Fungsi silsilah diabetes
            "Age": data['Age']  # Umur pasien
        }])


        # Normalisasi data input menggunakan scaler yang sama saat training (jika tersedia)
        if scaler is not None:
            try:
                input_data_scaled = scaler.transform(input_data)
            except Exception as e:
                logging.exception('Scaler.transform failed: %s', e)
                return jsonify({'error': 'Invalid input for scaler transform'}), 400
        else:
            input_data_scaled = input_data.values

        # Pastikan model tersedia
        if model is None:
            return jsonify({'error': 'Trained model (model.pkl) not found on server'}), 500

        # Melakukan prediksi dengan model yang sudah dimuat
        prediction = model.predict(input_data_scaled)

        # Mendapatkan probabilitas prediksi untuk setiap kelas (jika tersedia)
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_data_scaled)
        else:
            probabilities = [[None, None]]


        # Probabilitas positif dan negatif dalam bentuk persentase
        probability_negative = probabilities[0][0] * 100  # Probabilitas untuk kelas 0 (tidak diabetes) - dikali 100 untuk persentase
        probability_positive = probabilities[0][1] * 100  # Probabilitas untuk kelas 1 (diabetes) - dikali 100 untuk persentase


        # Prediksi output (0 atau 1, di mana 1 berarti positif diabetes)
        # Membuat pesan yang mudah dipahami berdasarkan hasil prediksi
        if prediction[0] == 1:
            result = f'Anda memiliki peluang menderita diabetes berdasarkan model KNN kami. Kemungkinan menderita diabetes adalah {probability_positive:.2f}%.'
        else:
            result = 'Hasil prediksi menunjukkan Anda kemungkinan rendah terkena diabetes.'


        # Kembalikan hasil prediksi dan probabilitas dalam bentuk JSON
        # jsonify() mengubah dictionary Python menjadi response JSON yang bisa dibaca oleh client
        return jsonify({
            'prediction': result,  # Pesan hasil prediksi
            'probabilities': {
                'negative': f"{probability_negative:.2f}%",  # Format 2 desimal untuk probabilitas negatif
                'positive': f"{probability_positive:.2f}%"  # Format 2 desimal untuk probabilitas positif
            }
        })


    except Exception as e:
        # Jika terjadi error (misalnya data tidak lengkap atau format salah)
        # Kembalikan pesan error dengan status code 400 (Bad Request)
        return jsonify({'error': str(e)}), 400




# Jalankan aplikasi Flask
# if __name__ == '__main__': memastikan kode ini hanya dijalankan jika file ini dieksekusi langsung
# (tidak dijalankan jika file ini diimpor sebagai module)
if __name__ == '__main__':
    app.run(debug=True)  # debug=True memberikan informasi error yang detail dan auto-reload saat development