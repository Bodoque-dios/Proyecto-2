import json
from gsuite.auth import get_credentials
from googleapiclient.discovery import build


class GoogleSheets:
    """
    Class to create and manage a Google Sheets resources.

    Args:
        auth_mode (str): Mode of authentication & authorization. Valid values are only 'server_side' and 'service_account'.
        client_secrets (str): The path to the credentials json file or credentials information in json format (only for auth_mode=service_account).
        delegated_email_address (str): Must be set if using 'service_account' as auth_mode. For domain-wide delegation, the email address of the user to for which to request delegated access.
        local_server_port (int): Must be set if using 'server_side' as auth_mode. The port for the local redirect server.
    """

    def __init__(self, auth_mode, client_secrets, delegated_email_address=None, local_server_port=None):
        # If modifying these scopes, delete the file token.pickle.
        #
        # Read more about oauth2 scopes:
        # https://developers.google.com/identity/protocols/oauth2/scopes
        oauth2_scopes = [
            "https://www.googleapis.com/auth/spreadsheets"
        ]

        credentials = get_credentials(
            auth_mode=auth_mode,
            client_secrets=client_secrets,
            oauth2_scopes=oauth2_scopes,
            delegated_email_address=delegated_email_address,
            local_server_port=local_server_port
        )

        # http://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.html
        self.sheets = build(
            serviceName="sheets",
            version="v4",
            credentials=credentials
        )

    def get_values(self, spreadsheet_id, range, major_dimension="ROWS", value_render_option="FORMATTED_VALUE"):
        """
        Returns a range of values from a spreadsheet.
        The caller must specify the spreadsheet ID and a range.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet to retrieve data from.
            range (str): The A1 notation of the values to retrieve.
            major_dimension (str): The major dimension that results should use. (default "ROWS")
            value_render_option: How values should be represented in the output. (default "FORMATTED_VALUE")

        Returns:
            dict:
                { # Data within a range of the spreadsheet.
                    "range": "A String", # The range the values cover, in A1 notation.
                        # For output, this range indicates the entire requested range,
                        # even though the values will exclude trailing rows and columns.
                        # When appending values, this field represents the range to search for a
                        # table, after which values will be appended.
                    "values": [ # The data that was read or to be written.  This is an array of arrays,
                        # the outer array representing all the data and each inner array
                        # representing a major dimension. Each item in the inner array
                        # corresponds with one cell.
                        #
                        # For output, empty trailing rows and columns will not be included.
                        #
                        # For input, supported value types are: bool, string, and double.
                        # Null values will be skipped.
                        # To set a cell to an empty value, set the string value to an empty string.
                    [
                        "",
                    ],
                    ],
                    "majorDimension": "A String", # The major dimension of the values.
                        #
                        # For output, if the spreadsheet data is: `A1=1,B1=2,A2=3,B2=4`,
                        # then requesting `range=A1:B2,majorDimension=ROWS` will return
                        # `[[1,2],[3,4]]`,
                        # whereas requesting `range=A1:B2,majorDimension=COLUMNS` will return
                        # `[[1,3],[2,4]]`.
                        #
                        # For input, with `range=A1:B2,majorDimension=ROWS` then `[[1,2],[3,4]]`
                        # will set `A1=1,B1=2,A2=3,B2=4`. With `range=A1:B2,majorDimension=COLUMNS`
                        # then `[[1,2],[3,4]]` will set `A1=1,B1=3,A2=2,B2=4`.
                        #
                        # When writing, if this field is not set, it defaults to ROWS.
                }
        """

        return self.sheets.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range,
            majorDimension=major_dimension,
            valueRenderOption=value_render_option
        ).execute()
