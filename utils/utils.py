from dotenv import load_dotenv
import os

def load_environment_variables(env_file=None):
    """
    Loads environment variables from a .env file and returns them as a dictionary.

    :param env_file: Optional path to a custom .env file.
    :return: Dictionary containing required Zscaler API credentials and configurations.
    """
    if env_file:
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()
    client_id = os.getenv("ZSCALER_CLIENT_ID",None)
    client_secret = os.getenv("ZSCALER_CLIENT_SECRET",None)
    vanity_domain = os.getenv("ZSCALER_VANITY_DOMAIN",None)
    customer_id = os.getenv("ZPA_CUSTOMER_ID", os.getenv("ZSCALER_CUSTOMER_ID", None))
    #zcc_client_id = os.getenv("ZCC_CLIENT_ID",None)
    #zcc_client_secret = os.getenv("ZCC_CLIENT_SECRET",None)


    if not client_id or not client_secret or not vanity_domain or not customer_id:
        raise ValueError(
            "Missing required environment variables. Ensure .env file contains 'ZSCALER_CLIENT_ID', "
            "'ZSCALER_CLIENT_SECRET', 'ZSCALER_VANITY_DOMAIN', and 'ZPA_CUSTOMER_ID'."
        )
    
    return_obj = {}

    return_obj['clientId'] = client_id
    return_obj['clientSecret'] = client_secret
    return_obj['vanityDomain'] = vanity_domain
    return_obj['customerId'] = customer_id
    return_obj['logging'] = { "enable" : False, "verbose": False}

    return return_obj

## End load_environment_variables