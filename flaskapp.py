from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dbCode import *
'''
# get items_list
items_list = get_list_of_dictionaries(category)
return render_template('display_items.html', items=items_list)
'''

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone


@app.route('/')
def home():
    query = """
        SELECT name, continent, population
        FROM country
        ORDER BY population DESC
        LIMIT 10;   
    """
    countries = execute_query(query)
    return render_template('home.html', results=countries)


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form.get('first_name')
        #session['username'] = first_name
        last_name = request.form.get('last_name')
        city = request.form['city']
        user = {
            'first_name': first_name,
            'last_name': last_name,
            'city': city
        }
        table.put_item(Item=user)
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("First Name:", first_name, ":", "Last Name:", last_name, ":", "City:", city)
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/display-users')
def display_users():
    key ={"First Name":session['first_name']}
    response = table.get_item(Key=key)
    return render_template('display_users.html', users = key)


@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first name']
        last_name = request.form['last name']
        

        print("Name:", first_name, last_name)
        
        flash('User deleted successfully!', 'warning')  # options include: success, error, warning, info
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['firstname']
        session['username'] = first_name
        last_name = request.form['lastname']
        city = request.form['city']
        table.update_item(
            key ={"first_name":first_name},
            UpdateExpression = "SET city = list_append(city, :r)",
            ExpressionAttributeValues = {':r': [city],})
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("First Name:", first_name, ":", "Last Name:", last_name, ":", "City:", city)
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
