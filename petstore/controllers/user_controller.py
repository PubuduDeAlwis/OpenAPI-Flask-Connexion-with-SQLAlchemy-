import connexion
import six

from openapi_server.models.user import User  # noqa: E501
from openapi_server import util
from openapi_server.orm import petstore
from werkzeug.security import generate_password_hash, check_password_hash


def create_user():  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
        id = body.id
        id_user = petstore.User.query.filter_by(id=id).first()
        if id is None:
            return 'User ID is Required', 404
        if id_user:
            return 'User Already Exists', 409
        username=body.username
        user = petstore.User.query.filter_by(username=username).first()
        if username is None:
            return 'User Name is Required', 404
        if user:
            return 'User Name is Already Exists', 409
        firstname = body.first_name
        lastname = body.last_name
        email = body.email
        password = generate_password_hash(body.password, method='sha256')
        phone = body.phone
        user_status = body.user_status

        new_user = petstore.User(id, username, firstname, lastname, email, password, phone, user_status)
        petstore.db.session.add(new_user)
        petstore.db.session.commit()

        return body


def create_users_with_array_input():  # noqa: E501
    """Creates list of users with given input array

     # noqa: E501

    :param body: List of user object
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [User.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

        for user in body:
            id = user.id
            id_user = petstore.User.query.filter_by(id=id).first()
            if id is None:
                return 'User ID is Required', 404
            if id_user:
                return 'User Already Exists', 409
            username = user.username
            user_n = petstore.User.query.filter_by(username=username).first()
            if username is None:
                return 'User Name is Required', 404
            if user_n:
                return "User Already Exists", 409
            firstname = user.first_name
            lastname = user.last_name
            email = user.email
            password = generate_password_hash(user.password)
            phone = user.phone
            user_status = user.user_status

            new_user = petstore.User(id, username, firstname, lastname, email, password, phone, user_status)
            petstore.db.session.add(new_user)
            petstore.db.session.commit()

        return body


def create_users_with_list_input():  # noqa: E501
    """Creates list of users with given input array

     # noqa: E501

    :param body: List of user object
    :type body: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = [User.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
        for user in body:
            id = user.id
            user_id = petstore.User.query.filter_by(id=id).first()
            if id is None:
                return 'User ID is Required', 404
            if user_id:
                return 'User ID Already Exists', 409
            username = user.username
            user_n = petstore.User.query.filter_by(username=username).first()
            if username is None:
                return 'User Name is Required', 404
            if user_n:
                return 'User Name Already Exists', 409
            firstname = user.first_name
            lastname = user.last_name
            email = user.email
            password = generate_password_hash(user.password)
            phone = user.phone
            user_status = user.user_status

            new_user = petstore.User(id, username, firstname, lastname, email, password, phone, user_status)
            petstore.db.session.add(new_user)
            petstore.db.session.commit()

        return body


def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done by the logged in user. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    user_d = petstore.User.query.filter_by(username=username).first()
    if user_d:
        petstore.db.session.delete(user_d)
        petstore.db.session.commit()
        return 'User is Successfully Deleted', 200
    elif user_d is None:
        return 'User Does Not Exists', 404


def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing. 
    :type username: str

    :rtype: User
    """
    user = petstore.User.query.filter_by(username=username).first()
    if user:
        return petstore.user_schema.jsonify(user)
    else:
        return 'User does not exists', 404


def login_user(username, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """
    user = petstore.User.query.filter_by(username=username).first()
    if user is None:
        return "User Does Not Exists", 404
    if user.username == username and check_password_hash(user.password, password):
        return petstore.user_schema.jsonify(user), 200
    else:
        return "Invalid Username or Password", 401


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by the logged in user. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    user_u = petstore.User.query.filter_by(username=username).first()
    if connexion.request.is_json:  # noqa: E501
        if user_u:
            if body['id'] is None:
                return 'User ID is Required', 404
            user_id = petstore.User.query.filter_by(id=body['id']).first()
            if user_id and user_id.username != username:
                return 'User ID Already Exists', 409
            if body['username'] is None:
                return 'User Name is Required', 404
            user_n = petstore.User.query.filter_by(username=body['username']).first()
            if user_n and user_n.id is not user_id.id:
                return 'User Name Already Exists', 409
            user_u.username = body['username']
            user_u.firstname = body['firstName']
            user_u.lastname = body['lastName']
            user_u.email = body['email']
            user_u.password = generate_password_hash(body['password'], method='sha256')
            user_u.phone = body['phone']
            user_u.user_status = body['userStatus']

            petstore.db.session.commit()
            update_user = petstore.User.query.filter_by(username=body['username']).first()
            return petstore.user_schema.jsonify(update_user)
        else:
            return "User Does Not Exists", 404
