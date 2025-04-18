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

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Add user to database
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        Username = request.form['Username']
        City = request.form['City']
        user = {
            'Username': Username,
            'City': City
        }
        # Process the data (e.g., add it to a database)
        table.put_item(Item=user)
        print(f"DEBUG: Username = {Username}, City = {City}")
        flash('User added successfully!', 'success') 

        # Redirect to city_country upon successful submission
        return redirect(url_for('city_country'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/display-users')
def display_users():
    try:
        # Gather data in the table
        response = table.scan()
        users = response.get('Items', [])
    except Exception as e:
        # If there is no one in the table, flash error
        flash(f"Error fetching users: {str(e)}", "error")
        users = []
    return render_template('display_users.html', users=users)

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        Username = request.form.get('Username')
        try:
            # Process the data (e.g., delete it to a database)
            response = table.delete_item(Key={'Username': Username})
            print("User deleted:", response)
            flash('User deleted successfully!', 'success') 
            # Return to home if successful
            return redirect(url_for('home'))
        except Exception as e:
            print("Error deleting user from DynamoDB:", e)
            flash('Error deleting user. Please try again.', 'error')
            # Redirect to delete_user if username not found
            return redirect(url_for('delete_user'))
    else:
        return render_template('delete_user.html')

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # Extract form data
        Username = request.form['Username']
        City = request.form['City']
        # Process the data (e.g. update city in the database)
        table.update_item(
            Key ={"Username": Username},
            UpdateExpression = "SET City = :new_city",
            ExpressionAttributeValues = {':new_city': City})
        
        flash('User city changed successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('update_user.html')

@app.route('/city-country', methods=['GET', 'POST'])
def city_country():
    country_name = None

    if request.method == 'POST':
        city_input = request.form.get('City', '').strip()
        # Query to find the country a city is in
        query = """
            SELECT country.name
            FROM city
            JOIN country ON city.countrycode = country.code
            WHERE city.name = %s
            LIMIT 1;
        """
        result = execute_query(query, (city_input,))

        if result and len(result) > 0:
            country_name = result[0]['name']
        else:
            flash("City not found in the database.", "error")

    return render_template('city_country.html', country=country_name)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)