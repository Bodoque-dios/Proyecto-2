import os
import pickle
import json
from json.decoder import JSONDecodeError
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials(auth_mode, client_secrets, oauth2_scopes, delegated_email_address=None, local_server_port=None, token_file="token.pickle"):
    """
    A method to get a valid credentials to interact with Google API

    Args:
        auth_mode (str): Mode of authentication & authorization. Valid values are only 'server_side' and 'service_account'.
        client_secrets (str): The path to the credentials json file or credentials information in json format (only for auth_mode=service_account).
        oauth2_scopes (list of str): Scopes to request during the authorization grant.
        delegated_email_address (str): Must be set if using 'service_account' as auth_mode. For domain-wide delegation, the email address of the user to for which to request delegated access.
        local_server_port (int): Must be set if using 'server_side' as auth_mode. The port for the local redirect server.
        token_file (str): Used only if using 'server_side' as auth_mode. The path where to store and load a temporary credentials information. (default "token.pickle")

    Returns:
        google.auth.service_account.Credentials if 'service_account' as auth_mode else google.oauth2.credentials.Credentials
    """

    server_side = "server_side"
    service_account = "service_account"

    credentials = None
    if auth_mode == server_side:
        if local_server_port is None:
            raise ValueError(
                "'local_server_port' argument must be set if 'auth_mode' is set to '{}'".format(
                    server_side
                )
            )
        else:
            credentials = server_side_web_apps_auth(
                client_secrets_file=client_secrets,
                oauth2_scopes=oauth2_scopes,
                local_server_port=local_server_port,
                token_file=token_file
            )
    elif auth_mode == service_account:
        if delegated_email_address is None:
            raise ValueError(
                "'delegated_email_address' argument must be set if 'auth_mode' is set to '{}'".format(
                    service_account
                )
            )
        else:
            credentials = service_account_auth(
                client_secrets=client_secrets,
                oauth2_scopes=oauth2_scopes,
                delegated_email_address=delegated_email_address
            )
    else:
        raise ValueError(
            "'auth_mode' argument only allows '{server_side}' or '{service_account}' as input".format(
                server_side=server_side,
                service_account=service_account
            )
        )

    return credentials


def service_account_auth(client_secrets, oauth2_scopes, delegated_email_address):
    """
    Creates a Credentials instance from a service account json file.

    Args:
        client_secrets (str): The path to the credentials json file or credentials information in json format.
        oauth2_scopes (list of str): Scopes to request during the authorization grant.
        delegated_email_address (str): For domain-wide delegation, the email address of the user to for which to request delegated access.

    Returns:
        google.auth.service_account.Credentials: Service account credentials
    """

    try:
        data = json.loads(client_secrets)

        # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html
        return Credentials.from_service_account_info(
            data,
            scopes=oauth2_scopes,
            subject=delegated_email_address
        )
    except JSONDecodeError:
        data = client_secrets

        # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html
        return Credentials.from_service_account_file(
            client_secrets,
            scopes=oauth2_scopes,
            subject=delegated_email_address
        )


def server_side_web_apps_auth(client_secrets_file, oauth2_scopes, local_server_port, token_file):
    """
    Private method to authorize to Google using Oauth2

    Args:
        client_secrets_file (str): The path to the client secrets *.json file.
        oauth2_scopes (list of str): The list of oauth2 scopes to request during the flow.
        local_server_port (int): The port for the local redirect server.
        token_file (str): The path where to store and load a temporary credentials information

    Returns:
        google.oauth2.credentials.Credentials: credential information
    """

    # Initialize credentials
    credentials = None

    # The file token.pickle stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file=client_secrets_file,
                scopes=oauth2_scopes
            )
            credentials = flow.run_local_server(port=local_server_port)

        # Save the credentials for the next run
        with open(token_file, "wb") as token:
            pickle.dump(credentials, token)

    return credentials
