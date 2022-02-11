from celery_demo import create_app, get_flashed_messages, render_template, url_for, session, request, flash, redirect
from celery import Celery
from flask_mail import Message, Mail



app = create_app()
mail = Mail(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_email(email_msg):
    #Async function to send an email with Flask-Mail
    msg_sub = Message(email_msg['subject'],
    email_sender = app.config['MAIL_DEFAULT_SENDER'],
    recipient = [email_msg['to']])
    msg_sub.body = email_msg['body']
    with app.app_context():
        mail.send(msg_sub)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email # Note: We saved the user's value in the text field in the session to remember it after the page reloads.
    # sends this content
    email_msg = {
        'subject': 'Testing Celery with Flask',
        'to': email,
        'body': 'Testing background task with Celery'
    }
    if request.form['submit'] == 'Send':
        # sends the email content to the backgraound function
        send_email.delay(email_msg)
        flash('Sending email to {0}'.format(email))
    else:
        flash('No Email sent')

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)