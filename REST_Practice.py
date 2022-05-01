'''
    @Author: Viney Khaneja
    @Date: 2022-04-29 21:12
    @Last Modified by: Viney Khaneja
    @Last Modified time: None
    @Title : Implementing REST using Flask Framework
'''

# Importing required modules
from flask import Flask, request, make_response
from flask_restful import Api
from werkzeug.exceptions import HTTPException, Aborter
import json

# Initializing Flask for implementing API
app = Flask(__name__)
api = Api(app)

# Loading all data of Json file acted a a database as of now.
with open('Supporting_Data.json') as read_data:
    supporting_data = json.load(read_data)


@app.route("/Emp_Data", methods=['GET'])
def get():
    """
        Description: This function is to retrieve data from Specified URL
        Parameters: None, just defined router path.
        Returns: A dictionary of requested data and response code to client
    """
    try:
        return make_response(supporting_data, 200)
    except Exception as ex:
        print(ex)


@app.route("/Emp_Data/<string:emp_id>", methods=['GET'])
def get_emp_by_ID(emp_id):
    """
        Description: This function is to employee data by his or her id
        Parameters: Employee ID as mentioned in URL
        Returns: A Json Format description of employee
    """
    try:
        abort_if_id_not_exists(emp_id)
        return make_response(supporting_data[emp_id], 200)
    except Exception as ex:
        return handle_exception(ex)


@app.route("/Emp_Data/<string:emp_id>/name", methods=['GET'])
def get_empName_by_ID(emp_id):
    """
        Description: This function is to employee name by his or her id
        Parameters: Employee ID as mentioned in URL
        Returns: Name of Employee
    """
    try:
        abort_if_id_not_exists(emp_id)
        return make_response(supporting_data[emp_id]['firstName'], 200)
    except Exception as ex:
        return handle_exception(ex)


@app.route("/Emp_Data/post_json", methods=['POST'])
def post():
    """
        Description: This function is to create employee data as taken in form of URL
        Parameters: None
        Returns: Just adding an employee data in JSON File, if id already exists, then a descriptive message to user is sent
    """
    try:
        posted_data = json.loads(request.data)
        for key in posted_data:
            abort_if_id_exists(key)
            with open('Supporting_Data.json', "w") as write_data:
                supporting_data.update(posted_data)
                json.dump(supporting_data, write_data, indent=4)
            return make_response("Posted Successfully", 201)
    except Exception as ex:
        return handle_exception(ex)


@app.route("/Emp_Data/<string:emp_id>", methods=['PUT'])
def put(emp_id):
    """
        Description: This function is to update employee data as taken in form of URL
        Parameters: Emp ID
        Returns: Just updating an employee data in JSON File, if id not exists, then a descriptive message to user is sent
    """
    try:
        abort_if_id_not_exists(emp_id)
        put_data = json.loads(request.data)
        for key, value in put_data.items():
            supporting_data[emp_id][key] = value
        with open('Supporting_Data.json', "w") as write_data:
            json.dump(supporting_data, write_data, indent=4)
        return make_response("Updated Successfully", 202)
    except Exception as ex:
        return handle_exception(ex)


@app.route("/Emp_Data/<string:emp_id>", methods=['DELETE'])
def delete(emp_id):
    """
        Description: This function is to delete employee data as taken in form of URL
        Parameters: Emp ID
        Returns: Just deleting an employee data in JSON File, if id not exists, then a descriptive message to user is sent
    """
    try:
        abort_if_id_not_exists(emp_id)
        del supporting_data[emp_id]
        with open('Supporting_Data.json', "w+") as write_data:
            json.dump(supporting_data, write_data, indent=4)
        return make_response("Deleted Successfully", 202)
    except Exception as ex:
        return handle_exception(ex)


# Object of Aborted is made as imported from werkzeug.exceptions
abort = Aborter()


def abort_if_id_not_exists(id):
    """
        Description: This function is to abort request and send HTTP Status code with description, if id not exists.
        Parameters: Emp ID
        Returns: Returning HTTP Status code and Descriptive message for user.
    """
    if id not in supporting_data:
        abort(404, description="ID is not valid, Please enter correct ID")


def abort_if_id_exists(id):
    """
        Description: This function is to abort request and send HTTP Status code with description, if id exists already
        Parameters: Emp ID
        Returns: Returning HTTP Status code and Descriptive message for user.
    """
    if id in supporting_data:
        abort(403, description="ID Already exists, a copy with same id would also not be created")


@app.errorhandler(HTTPException)
def handle_exception(e):
    """
        Description: This function is to handle abort statements
        Parameters: Abort Status Code HTTP Exceptions
        Returns: Return JSON instead of HTML for HTTP errors.
    """
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run(debug=True)
