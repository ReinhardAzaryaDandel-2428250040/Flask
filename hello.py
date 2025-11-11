# import Flask module
from flask import Flask, render_template

# create Flask app instance (atur folder template ke 'views')
app = Flask(__name__, template_folder='views')


# define route for the root URL
@app.route('/')
def hello_world():
    # render halaman utama menggunakan main.html dan kirimkan title
    return render_template('main.html', title='Home')

# define route untuk about
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# define route untuk contact
@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/home')
def home():
    # juga layani /home ke halaman utama
    return render_template('main.html', title='Home')

  

# run the app
if __name__ == '__main__':
    app.run(debug=True)
