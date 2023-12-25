from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
app.template_folder = os.path.abspath('templates')

# Initialize a Pandas DataFrame to store values
data = pd.DataFrame(columns=['User', 'Message'])

@app.route('/')
def index():
    # Display the stored values in the DataFrame
    stored_values = data.to_html(index=False)
    return render_template('index.html', stored_values=stored_values)

@app.route('/send', methods=['POST'])
def send():
    user_message = request.form.get('message')

    # Add the entered value to the DataFrame
    data.loc[len(data)] = ['User', user_message]

    # Display the stored values in the DataFrame
    stored_values = data.to_html(index=False)
    return render_template('index.html', stored_values=stored_values)

if __name__ == '__main__':
    app.run()
