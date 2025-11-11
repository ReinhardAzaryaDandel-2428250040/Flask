# import Flask module
from flask import Flask, render_template

# create Flask app instance (atur folder template ke 'views')
app = Flask(__name__, template_folder='views')


# define route for the root URL
@app.route('/')
def hello_world():
    return render_template('main.html')

# define route untuk about
@app.route('/about')
def about():
    return render_template('about.html')
   
   # define route untuk contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# run the app
if __name__ == '__main__':
    app.run(debug=True)
