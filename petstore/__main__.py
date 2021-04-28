#!/usr/bin/env python
from openapi_server import encoder
from openapi_server import config


def main():

    config.connex_app.app.json_encoder = encoder.JSONEncoder
    config.connex_app.add_api('openapi.yaml',
                arguments={'title': 'Swagger Petstore'},
                pythonic_params=True)

    config.connex_app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
