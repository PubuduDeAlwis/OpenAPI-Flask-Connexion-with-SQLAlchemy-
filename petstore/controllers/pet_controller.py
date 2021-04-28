import connexion
import six

from openapi_server.models.category import Category  # noqa: E501
from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server.orm import petstore
from openapi_server import util


def add_pet():  # noqa: E501
    """Add a new pet to the store

     # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: Pet
    """
    if connexion.request.is_json:
        body = Pet.from_dict(connexion.request.get_json())  # noqa: E501
        id = body.id
        category_id = body.category.id
        category_name = body.category.name
        status = body.status
        name = body.name
        tags = body.tags
        photoURLs = body.photo_urls

        cat_id = petstore.Category.query.filter_by(id=category_id).first()
        cat_name = petstore.Category.query.filter_by(cat_name=category_name).first()

        if cat_id is None and cat_name is None:
            new_category = petstore.Category(category_id, category_name)
            petstore.db.session.add(new_category)
            petstore.db.session.commit()
        elif cat_id and cat_name is None:
            return "Category ID Already Exists. Can not assign to New Category", 409
        elif cat_id is None and cat_name:
            return "Category name is Already Exists. Can not assign to the ID", 409

        status = petstore.Status.query.filter_by(value=status).first()

        for tag in tags:
            tag_id = petstore.Tag.query.filter_by(id=tag.id).first()
            tag_n = petstore.Tag.query.filter_by(tag_name=tag.name).first()
            if tag_id is None and tag_n is None:
                new_tag = petstore.Tag(tag.id, tag.name)
                petstore.db.session.add(new_tag)
                petstore.db.session.commit()
            elif tag_id and tag_n is None:
                return "Tad ID Already Exists in {}. Can not Assign to New Tag Name".format(tag_id.tag_name), 409
            elif tag_id is None and tag_n:
                return "Tag Name is Already Exists in {}. Can not Assign to New Tag ID".format(tag_n.id), 409
        pet_id_exists = petstore.Pet.query.filter_by(id=id).first()
        pet_name_exists = petstore.Pet.query.filter_by(pet_name=name).first()
        if pet_id_exists:
            return "Pet ID is Already Exists", 409
        if pet_name_exists:
            return "Pet Name is Already Exists", 409
        category = petstore.Category.query.filter_by(id=category_id).first()
        new_pet = petstore.Pet(id, name, category.id, status.id)
        petstore.db.session.add(new_pet)
        petstore.db.session.commit()

        if tags:
            for tag in tags:
                tag_db = petstore.Tag.query.filter_by(tag_name=tag.name).first()
                pet = petstore.Pet.query.filter_by(pet_name=name).first()
                if tag_db and pet:
                    tag_db.tags.append(pet)
                    petstore.db.session.commit()
                elif tag is None and pet is None:
                    return "Pet and Tag Does Not Exists", 404
                elif pet is None:
                    return "Pet Does Not Exists", 404
                elif tag_db is None:
                    return "Tag Does Not Exists", 404

        if photoURLs:
            for photoURL in photoURLs:
                new_url = petstore.PhotoURL(photoURL, id)
                petstore.db.session.add(new_url)
                petstore.db.session.commit()

        return body, 200


def delete_pet(pet_id):  # noqa: E501
    """Deletes a pet

     # noqa: E501

    :param pet_id: Pet id to delete
    :type pet_id: int

    :rtype: Pet
    """
    pet = petstore.Pet.query.get(pet_id)
    photourls = petstore.PhotoURL.query.filter_by(pet_id=pet_id).all()
    for i in photourls:
        petstore.db.session.delete(pet)
    petstore.db.session.delete(pet)
    petstore.db.session.commit()
    return 'Pet is Deleted Successfully!', 200


def find_pets_by_status(status):  # noqa: E501
    """Finds Pets by status

    Multiple status values can be provided with comma separated strings # noqa: E501

    :param status: Status values that need to be considered for filter
    :type status: List[str]

    :rtype: List[Pet]
    """
    statusdb = petstore.Status.query.filter_by(value=status).first()
    pets = petstore.Pet.query.filter_by(status_id=statusdb.id).all()
    return petstore.pets_schema.jsonify(pets), 200


def find_pets_by_tags(tags):  # noqa: E501
    """Finds Pets by tags

    Muliple tags can be provided with comma separated strings. Use         tag1, tag2, tag3 for testing. # noqa: E501

    :param tags: Tags to filter by
    :type tags: List[str]

    :rtype: List[Pet]
    """
    for tag in tags:
        tagdb = petstore.Tag.query.filter_by(tag_name=tag).first()
        if tagdb is None:
            return "Tag Does Not Exists", 404
        pets = petstore.Pet.query.with_parent(tagdb)
        if pets is None:
            return "Pet Does Not Exists With This Tag", 404
        pets = petstore.pets_schema.dump(pets)
        return petstore.pets_schema.jsonify(pets), 200


def get_pet_by_id(pet_id):  # noqa: E501
    """Find pet by ID

    Returns a single pet # noqa: E501

    :param pet_id: ID of pet to return
    :type pet_id: int

    :rtype: Pet
    """
    pet = petstore.Pet.query.get(pet_id)
    if pet is None:
        return "Pet ID Does Not Exists!", 404
    else:
        return petstore.pet_schema.jsonify(pet)


def update_pet():  # noqa: E501
    """Update an existing pet

     # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: Pet
    """
    if connexion.request.is_json:
        body = Pet.from_dict(connexion.request.get_json())  # noqa: E501
        id = body.id
        name = body.name
        status = body.status
        category_id = body.category.id
        category_name = body.category.name
        tags = body.tags
        photoURLs = body.photo_urls
        pet_id = petstore.Pet.query.get(id)
        pet_n = petstore.Pet.query.filter_by(pet_name=name).first()

        if id is None:
            return "Pet ID is Required", 404

        if name is None:
            return "Pet Name is Required", 404

        if pet_n and pet_n.pet_name != pet_id.pet_name:
            return "Pet Name Already Exists", 409

        elif pet_id:
            statusdb = petstore.Status.query.filter_by(value=status).first()

            category_id_db = petstore.Category.query.filter_by(cat_name=category_name).first()
            category_name_db = petstore.Category.query.filter_by(id=category_id).first()

            if category_id_db is None and category_name_db is None:
                new_category = petstore.Category(category_id, category_name)
                petstore.db.session.add(new_category)
                petstore.db.session.commit()
            elif category_id_db and category_name_db is None:
                return "Category ID is Already Exists in Category Name = {}".format(category_id_db.cat_name), 409
            elif category_id_db is None and category_name_db:
                return "Category name is Already Exists in ID = {}".format(category_name_db.id), 409
            pet_id.pet_name = name
            pet_id.category_id = category_id
            pet_id.status_id = statusdb.id
            petstore.db.session.commit()

            if tags:
                for tag in tags:
                    tag_id = petstore.Tag.query.filter_by(id=tag.id).first()
                    tag_n = petstore.Tag.query.filter_by(tag_name=tag.name).first()
                    if tag_id is None and tag_n is None:
                        new_tag = petstore.Tag(tag.id, tag.name)
                        petstore.db.session.add(new_tag)
                        petstore.db.session.commit()
                    elif tag_id and tag_n is None:
                        return "Tad ID Already Exists in {}. Can not Assign to New Tag Name".format(
                            tag_id.tag_name), 409
                    elif tag_id is None and tag_n:
                        return "Tag Name is Already Exists in {}. Can not Assign to New Tag ID".format(tag_n.id), 409
                for tag in tags:
                    pet = petstore.Pet.query.filter_by(pet_name=name).first()
                    tag_db = petstore.Tag.query.filter_by(tag_name=tag.name).first()

                    if tag_db and pet:
                        tag_db.tags.append(pet)
                        petstore.db.session.commit()
                    elif tag is None and pet is None:
                        return "Pet and Tag Does Not Exists", 404
                    elif pet is None:
                        return "Pet Does Not Exists", 404
                    elif tag_db is None:
                        return "Tag Does Not Exists", 404

            if photoURLs:
                for photoURL in photoURLs:
                    url = petstore.PhotoURL.query.filter_by(url=photoURL).first()
                    if url is None:
                        new_url = petstore.PhotoURL(photoURL,id)
                        petstore.db.session.add(new_url)
                        petstore.db.session.commit()
        return body


def update_pet_with_form(pet_id, name=None, status=None):  # noqa: E501
    """Updates a pet in the store with form data

       # noqa: E501

      :param pet_id: ID of pet that needs to be updated
      :type pet_id: int
      :param name: Name of pet that needs to be updated
      :type name: str
      :param status: Status of pet that needs to be updated
      :type status: str

      :rtype: None
      """
    pet_id = petstore.Pet.query.filter_by(id=pet_id).first()
    pet_n = petstore.Pet.query.filter_by(pet_name=name).first()
    if pet_id is None:
        return "Pet with this ID Does Not Exists", 404

    if pet_id and pet_n and pet_id.pet_name != pet_n.pet_name :
        return "Pet Name is Already Exists with the ID {}".format(pet_n.pet_name), 409

    if pet_id:
        if name is not None:
            pet_id.pet_name = name
        status = petstore.Status.query.filter_by(value=status).first()
        pet_id.status_id = status.id
        petstore.db.session.commit()

        return 'Pet is Updated Successfully', 200


def upload_file(pet_id, body=None):  # noqa: E501
    """uploads an image

     # noqa: E501

    :param pet_id: ID of pet to update
    :type pet_id: int
    :param body: 
    :type body: str

    :rtype: Pet
    """
    pet = petstore.Pet.query.filter_by(id=pet_id).first()

    if pet:
        url = petstore.PhotoURL.query.filter_by(url=body).first()
        if url is None:
            new_url=petstore.PhotoURL(body, pet_id)
            petstore.db.session.add(new_url)
            petstore.db.session.commit()
            return 'URL added successfully', 200
        else:
            return 'URL Exists', 409
