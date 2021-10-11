import flask
from flask import jsonify
from flask import request, make_response
from jinja2.loaders import ChoiceLoader, ModuleLoader
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
#imported the sql file so that I could utilize the connection function as well as thequery functions
#imported the flask library to be able to fulfill the JSON requirements

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allows errors to be shown in broswer

#CRUD for User_Profile Table
#Creating connection to the user profile table in the AWS database
#for each route, the naming convention is to have different names for endpoints, regardless of the method used
@app.route('/api-fp1/user_profile',methods=['GET'])
def api_users():
    #this route displays all the user profiles, I used this method for testing pruposes
    conn = create_connection("cis3368.cemoodnlbqm2.us-east-2.rds.amazonaws.com", "admin","fall21CIS#", "cis3368fall21")
    sql = "SELECT * FROM user_profile"
    user_profile = execute_read_query(conn, sql)
    #using the sql statement to select users, I did a read query to make them accessible
    results = []
    #made results an empty dictionary to store the users in so that I could return them as a JSON object
    for user in user_profile:
        results.append(user)
    return jsonify(results)

#new route for adding user to user profile table using POST method, 
#more intuitive for me to use each method depending on the intended task, rather than
#using GET for all of them
@app.route('/api-fp1/add_user',methods=['POST'])
#defintion for using add_user, begins with connection to db with necessary credentials
def api_add_user():
    conn = create_connection("cis3368.cemoodnlbqm2.us-east-2.rds.amazonaws.com", "admin","fall21CIS#", "cis3368fall21")
    request_data = request.get_json()
    #user input in postman for adding new user with their info
    #only ask for first and last name because user ID is automatically generated when a new user is added to the table
    first_name = request_data['first_name']
    last_name = request_data['last_name']
    #use CRUD OPS sql statements in order to change the database, the values are strings so they are in quotes
    #I used the same name in the python code as the ones already in the db just to keep things simple 
    #and make it clear which variable is being represented
    sql_query = "INSERT INTO user_profile (first_name, last_name) VALUES ('%s', '%s')" % (first_name, last_name)
    execute_query(conn, sql_query)
    #return statement shows up to user so that we know there were no erros and the query was carried through
    return "POST successful"
    

#new route for updating user in user profile table using PUT method
@app.route('/api-fp1/update_user',methods=['PUT'])
#update user defintion begins with the db connection with necessary credentials to access it
def api_update_user():
    conn = create_connection("cis3368.cemoodnlbqm2.us-east-2.rds.amazonaws.com", "admin","fall21CIS#", "cis3368fall21")
    request_data = request.get_json()
    #user must first enter ID, so that verify their identity and only have the ability to edit their own profile
    which_user = request_data['user_id']
    #then user must input first and last name, editing one or both to update their profile
    first_name = request_data['first_name']
    last_name = request_data['last_name']
    #once user has changed their deisred name the queries run and update the user_profile table
    #one query for first name and one for last name because doing 2 SET statements within one query did not update the info
    sql_query1 = """UPDATE user_profile SET first_name = '%s' WHERE user_id = %s """ % (first_name, which_user)
    sql_query2 = """UPDATE user_profile SET last_name = '%s' WHERE user_id = %s """ % (last_name, which_user)
    #this is an execute query and not a execute read query because we don't need to 
    #read and return any info to the user, just update internally in the db
    #there is one eexecute_query for each of changes that need to be made
    execute_query(conn, sql_query1)
    execute_query(conn, sql_query2)
    #finally, there is a return statement to let the user know the changes were made
    return 'PUT successful'

#new route for deleting user from user profile table using DELETE method
@app.route('/api-fp1/delete_user',methods=['DELETE'])
#delete user function also begins with the db connection
def api_delete_user():
    conn = create_connection("cis3368.cemoodnlbqm2.us-east-2.rds.amazonaws.com", "admin","fall21CIS#", "cis3368fall21")
    request_data = request.get_json()
    #the user must input their own ID in order to delete their account, this is to ensure
    #that others don't have the ability to delete another users accounts
    user_id = request_data['user_id']
    #the user ID is then used in the sql DELETE statement and the query is run
    delete_statement = "DELETE FROM user_profile WHERE user_id = %s" % (user_id)
    execute_query(conn,delete_statement)
    #once the users account has been deleted, this return message lets them know
    return 'DELETE successful'

#CRUD for Restaurant Tables
#new route for adding a restaurant using POST method
##@app.route('/api-fp1/add_restaurant',methods=['POST'])
#def api_add_restaurant():
    #request_data = request.get_json()
    #newid = request_data['id']
    #newmake = request_data['make']
    #newmodel = request_data['model']
    #newyear = request_data['year']
    #newcolor = request_data['color']
    #restaurant.append({'id':newid,'make':newmake,'model':newmodel,'year':newyear,'color':newcolor})
    #return 'POST successful'

#new route for updating restaurant in restaurant table using PUT method
#@app.route('/api-fp1/update_restaurant',methods=['PUT'])
#def api_update_restaurant():
    #request_data = request.get_json()
    #new_user_id = request_data['id']
    #new_fname = request_data['first_name']
    #new_lname = request_data['last_name']
    #restaurant.append({'id':new_user_id,'first_name':new_fname,'last_name':new_lname})
    #return 'POST successful'

#new route for deleting restaurant from restaurant table using DELETE method
#@app.route('/api-fp1/delete_restaurant',methods=['DELETE'])
#def api_delete_restaurant():
    #request_data = request.get_json()
    #new_user_id = request_data['id']
    #new_fname = request_data['first_name']
    #new_lname = request_data['last_name']
    #restaurant.append({'id':new_user_id,'first_name':new_fname,'last_name':new_lname})
    #return 'POST successful'

#Random Restaurant Selection

app.run()

