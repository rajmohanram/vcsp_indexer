from app.extensions import db
import os, sys, logging


def get_conn_vars():
    """
    Get connection variables from OS Environment variables.
    :return:
    """
    connection_vars = {
        'region_name': os.environ.get('region_name'),
        'endpoint_url': os.environ.get('endpoint_url'),
        'aws_access_key_id': os.environ.get('access_key_id'),
        'aws_secret_access_key': os.environ.get('secret_access_key')
    }

    return connection_vars


def validate_env_vars():
    """
    Validate the MinIO connection environment variables.
    Terminate application if all required Env. variables are not set.
    :param logging: Custom logging handler
    :return: connection_vars
    """
    logging.info("Validating MinIO connection environment variables.")

    connection_vars = get_conn_vars()

    connection_vars_none = []

    for name, value in connection_vars.items():
        if value is None or not value:
            connection_vars_none.append(name)

    if connection_vars_none:
        logging.error("Following MinIO connection variables are set to None")
        for name in connection_vars_none:
            logging.error(f"'{name}' is not set.")
        logging.info("Exiting the application.")
        sys.exit()

    for name, value in connection_vars.items():
        if 'access_key' in name:
            logging.info(f"Env. variable '{name}': *********")
        else:
            logging.info(f"Env. variable '{name}': {value}")

