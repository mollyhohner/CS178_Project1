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

        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/display-users')
def display_users():
    try:
        response = table.scan()
        users = response.get('Items', [])
    except Exception as e:
        flash(f"Error fetching users: {str(e)}", "error")
        users = []

    return render_template('display_users.html', users=users)

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        Username = request.form.get('Username')

        if not Username:
            flash("Username is required to delete a user."),
            return redirect(url_for('delete_user'))
    
        try:
            response = table.get_item(Key={'Username':Username})

            if 'Item' not in response:
                flash(f"User '{Username}' not found.", 'error')
                return redirect(url_for('delete_user'))

            # Proceed with delete
            table.delete_item(Key={'Username': Username})
            flash(f"User '{Username}' deleted successfully!", 'warning')

        except Exception as e:
            flash(f"Error deleting user: {str(e)}", "error")

        '''      
        # Delete user from database
        if Username:
            table.delete_item(Key={'Username': Username})
        flash('User deleted successfully!', 'warning')  # options include: success, error, warning, info'''
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    # Render the form page if the request method is GET
    return render_template('delete_user.html')

print(table.key_schema)
@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        # Extract form data
        Username = request.form['Username']
        City = request.form['City']
        table.update_item(
            key ={"Username":Username},
            UpdateExpression = "SET City = list_append(City, :r)",
            ExpressionAttributeValues = {':r': [City],})
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Username:", Username, ":", "City:", City)
        
        flash('User added successfully!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
