from flask import Flask, render_template, url_for, request, redirect
import csv
from datetime import datetime
from flask_mail import Mail, Message


app = Flask(__name__)
print(__name__)


app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'berny@fastmail.com'
app.config['MAIL_PASSWORD'] = 'w5enmhucdzy93yfj'
app.config['MAIL_USE_TLS'] =  False
app.config['MAIL_USE_SSL'] = True     

mail = Mail(app)
crt_dTime = datetime.now()



@app.route('/')
def my_home():
    return render_template('index.html')


def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>', methods=['GET', 'POST'])
def html_page(page_name):
    return render_template(page_name)

#need to specify the form 'action=' name to let python know where to get thee info from
@app.route('/submit_form', methods=['POST'])
def contact_form():
    #gets input from user in contact.html form
    usr_input_email = request.form.get('email')
    usr_input_subject = request.form.get('subject')
    usr_input_message = request.form.get('message')

    msg = Message(usr_input_subject, sender= usr_input_email, recipients=['berny@fastmail.com'])
    msg.body = usr_input_message
    mail.send(msg)
    return render_template('thankyou.html')


def write_to_file(data):
    with open('database.txt',mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data): 
    with open('database.csv',newline='', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([crt_dTime ,email,subject,message])
        

#to submit user data contact form
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong try again'
    

