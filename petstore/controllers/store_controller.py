import connexion
import six

from openapi_server.models.order import Order  # noqa: E501
from openapi_server.orm import petstore
from openapi_server import util


def delete_order(order_id):  # noqa: E501
    """Delete purchase order by ID

    For valid response try integer IDs with positive integer value.         Negative or non-integer values will generate API errors # noqa: E501

    :param order_id: ID of the order that needs to be deleted
    :type order_id: int

    :rtype: None
    """
    order = petstore.Order.query.get(order_id)
    if order is None:
        return 'Order Does Not Exists', 404
    if order:
        petstore.db.session.delete(order)
        petstore.db.session.commit()
        return 'Order = {} is Deleted Successfully'.format(order_id), 200


def get_inventory():  # noqa: E501
    """Returns pet inventories by status

    Returns a map of status codes to quantities # noqa: E501


    :rtype: Dict[str, int]
    """
    store = petstore.Order.query.all()
    return petstore.pets_schema.jsonify(store)


def get_order_by_id(order_id):  # noqa: E501
    """Find purchase order by ID

    For valid response try integer IDs with value &gt;&#x3D; 1 and &lt;&#x3D; 10.         Other values will generated exceptions # noqa: E501

    :param order_id: ID of pet that needs to be fetched
    :type order_id: int

    :rtype: Order
    """
    order = petstore.Order.query.filter_by(id=order_id).first()
    if order is None:
        return 'Order With ID = {} Does Not Exists'.format(order_id), 404
    if order:
        return petstore.order_schema.jsonify(order), 200


def place_order(body):  # noqa: E501
    """Place an order for a pet

     # noqa: E501

    :param body: order placed for purchasing the pet
    :type body: dict | bytes

    :rtype: Order
    """
    if connexion.request.is_json:
        body = Order.from_dict(connexion.request.get_json())  # noqa: E501
        id = body.id
        if id is None:
            return 'Order ID is Required',404
        order = petstore.Order.query.filter_by(id=id).first()
        if order:
            return 'Order Already Exists', 409
        pet_id = body.pet_id
        if body.pet_id is None:
            return 'Pet ID is Required to Place a Order', 404
        pet = petstore.Pet.query.filter_by(id=body.pet_id).first()
        if pet is None:
            return 'Pet With The ID Does Not Exists', 404
        quantity = body.quantity
        shipdate = body.ship_date
        complete = body.complete
        status = petstore.Status.query.filter_by(value=body.status).first()
        status_id = status.id
        new_order = petstore.Order(id, pet_id, quantity, shipdate, complete, status_id)
        petstore.db.session.add(new_order)
        petstore.db.session.commit()
        return petstore.order_schema.jsonify(new_order), 200
