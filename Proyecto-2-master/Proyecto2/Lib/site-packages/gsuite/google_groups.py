from gsuite.auth import get_credentials
from googleapiclient.discovery import build


class GoogleGroups:
    """
    Class to create and manage a Google Groups resource, its members, and its settings.

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
            "https://www.googleapis.com/auth/admin.directory.group",
            "https://www.googleapis.com/auth/admin.directory.group.member",
            "https://www.googleapis.com/auth/apps.groups.settings"
        ]

        credentials = get_credentials(
            auth_mode=auth_mode,
            client_secrets=client_secrets,
            oauth2_scopes=oauth2_scopes,
            delegated_email_address=delegated_email_address,
            local_server_port=local_server_port
        )

        # http://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.html
        self.admin_directory = build(
            serviceName="admin",
            version="directory_v1",
            credentials=credentials
        )

        # http://googleapis.github.io/google-api-python-client/docs/dyn/groupssettings_v1.html
        self.groupsettings = build(
            serviceName="groupssettings",
            version="v1",
            credentials=credentials
        )

    def create_group(self, email, name, description):
        """
        Create a group.

        Docs: http://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.groups.html

        Args:
            email (str):       The group's email address.
                               If your account has multiple domains, select the appropriate domain for the email address.
                               The email must be unique. This property is required when creating a group.
            name (str):        The group's display name.
            description (str): An extended description to help users determine the purpose of a group. Maximum length is 4,096 characters.

        Returns:
            dict:
                { # JSON template for Group resource in Directory API.
                    "nonEditableAliases": [ # List of non editable aliases (Read-only)
                        "A String",
                    ],
                    "kind": "admin#directory#group", # Kind of resource this is.
                    "description": "A String", # Description of the group
                    "name": "A String", # Group name
                    "adminCreated": True or False, # Is the group created by admin (Read-only) *
                    "directMembersCount": "A String", # Group direct members count
                    "id": "A String", # Unique identifier of Group (Read-only)
                    "etag": "A String", # ETag of the resource.
                    "email": "A String", # Email of Group
                    "aliases": [ # List of aliases (Read-only)
                            "A String",
                    ],
                }
        """

        body = {
            "email": email,
            "name": name,
            "description": description
        }
        return self.admin_directory.groups().insert(body=body).execute()

    def get_group(self, group_key):
        """
        Get a group.

        Docs: http://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.groups.html

        Args:
            group_key (str): Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID.

        Returns:
            dict:
                { # JSON template for Group resource in Directory API.
                    "nonEditableAliases": [ # List of non editable aliases (Read-only)
                        "A String",
                    ],
                    # Kind of resource this is.
                    "kind": "admin#directory#group",
                    "description": "A String", # Description of the group
                    "name": "A String", # Group name
                    # Is the group created by admin (Read-only) *
                    "adminCreated": True or False,
                    "directMembersCount": "A String", # Group direct members count
                    "id": "A String", # Unique identifier of Group (Read-only)
                    "etag": "A String", # ETag of the resource.
                    "email": "A String", # Email of Group
                    "aliases": [ # List of aliases (Read-only)
                        "A String",
                    ],
                }
        """

        return self.admin_directory.groups().get(groupKey=group_key).execute()

    def delete_group(self, group_key):
        """
        Delete a group.

        Docs: http://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.groups.html

        Args:
            group_key (str): Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID.
        """

        self.admin_directory.groups().delete(groupKey=group_key).execute()

    def update_group_settings(self, group_email, body=None):
        """
        Updates an existing group's settings.

        Args:
            group_email (str):  The group's email address.
            body (dict):        https://developers.google.com/admin-sdk/groups-settings/v1/reference/groups (default to None but will be overriden)

        Returns:
            dict: https://developers.google.com/admin-sdk/groups-settings/v1/reference/groups
        """

        if body is None:
            body = {
                "kind": "groupsSettings#groups",
                "whoCanJoin": "CAN_REQUEST_TO_JOIN",
                "whoCanViewMembership": "ALL_IN_DOMAIN_CAN_VIEW",
                "whoCanViewGroup": "ALL_MEMBERS_CAN_VIEW",
                "whoCanInvite": "ALL_MANAGERS_CAN_INVITE",
                "whoCanAdd": "ALL_MANAGERS_CAN_ADD",
                "allowExternalMembers": "false",
                "whoCanPostMessage": "ANYONE_CAN_POST",
                "allowWebPosting": "false",
                "maxMessageBytes": 26214400,
                "isArchived": "true",
                "archiveOnly": "false",
                "messageModerationLevel": "MODERATE_NONE",
                "spamModerationLevel": "MODERATE",
                "replyTo": "REPLY_TO_IGNORE",
                "customReplyTo": "",
                "includeCustomFooter": "false",
                "customFooterText": "",
                "sendMessageDenyNotification": "false",
                "defaultMessageDenyNotificationText": "",
                "showInGroupDirectory": "false",
                "allowGoogleCommunication": "false",
                "membersCanPostAsTheGroup": "false",
                "messageDisplayFont": "DEFAULT_FONT",
                "includeInGlobalAddressList": "true",
                "whoCanLeaveGroup": "ALL_MEMBERS_CAN_LEAVE",
                "whoCanContactOwner": "ALL_IN_DOMAIN_CAN_CONTACT",
                "whoCanAddReferences": "NONE",
                "whoCanAssignTopics": "NONE",
                "whoCanUnassignTopic": "NONE",
                "whoCanTakeTopics": "NONE",
                "whoCanMarkDuplicate": "NONE",
                "whoCanMarkNoResponseNeeded": "NONE",
                "whoCanMarkFavoriteReplyOnAnyTopic": "NONE",
                "whoCanMarkFavoriteReplyOnOwnTopic": "NONE",
                "whoCanUnmarkFavoriteReplyOnAnyTopic": "NONE",
                "whoCanEnterFreeFormTags": "NONE",
                "whoCanModifyTagsAndCategories": "NONE",
                "favoriteRepliesOnTop": "false",
                "whoCanApproveMembers": "ALL_MANAGERS_CAN_APPROVE",
                "whoCanBanUsers": "OWNERS_AND_MANAGERS",
                "whoCanModifyMembers": "OWNERS_AND_MANAGERS",
                "whoCanApproveMessages": "OWNERS_AND_MANAGERS",
                "whoCanDeleteAnyPost": "OWNERS_AND_MANAGERS",
                "whoCanDeleteTopics": "OWNERS_AND_MANAGERS",
                "whoCanLockTopics": "OWNERS_AND_MANAGERS",
                "whoCanMoveTopicsIn": "OWNERS_AND_MANAGERS",
                "whoCanMoveTopicsOut": "OWNERS_AND_MANAGERS",
                "whoCanPostAnnouncements": "OWNERS_AND_MANAGERS",
                "whoCanHideAbuse": "NONE",
                "whoCanMakeTopicsSticky": "NONE",
                "whoCanModerateMembers": "OWNERS_AND_MANAGERS",
                "whoCanModerateContent": "OWNERS_AND_MANAGERS",
                "whoCanAssistContent": "NONE",
                "customRolesEnabledForSettingsToBeMerged": "false",
                "enableCollaborativeInbox": "false",
                "whoCanDiscoverGroup": "ALL_MEMBERS_CAN_DISCOVER"
            }

        return self.groupsettings.groups().patch(groupUniqueId=group_email, body=body).execute()

    def get_member(self, group_key, member_key):
        """
        Get existing member

        Args:
            group_key (str): Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID.
            member_key (str): Identifies the group member in the API request. A group member can be a user or another group. The value can be the member's (group or user) primary email address, alias, or unique ID.

        Returns:
            dict: 
                { # JSON template for Member resource in Directory API.
                    "status": "A String", # Status of member (Immutable)
                    "kind": "admin#directory#member", # Kind of resource this is.
                    "delivery_settings": "A String", # Delivery settings of member
                    "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
                    "etag": "A String", # ETag of the resource.
                    "role": "A String", # Role of member
                    "type": "A String", # Type of member (Immutable)
                    "email": "A String", # Email of member (Read-only)
                }
        """
        return self.admin_directory.members().get(groupKey=group_key, memberKey=member_key).execute()

    def add_member(self, group_key, member_email, member_role, member_type="USER", delivery_settings="ALL_MAIL"):
        """
        Adds a user to the specified group.

        Args:
            group_key (str):    Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID.
            member_email (str): The member's email address. A member can be a user or another group. This property is required when adding a member to a group.
                                The email must be unique and cannot be an alias of another group. If the email address is changed,
                                the API automatically reflects the email address changes.
            member_role (str):  The member's role in a group. The API returns an error for cycles in group memberships.
                                Acceptable values are:
                                - "MANAGER": This role is only available if the Google Groups for Business is enabled using the Admin console.
                                             A MANAGER role can do everything done by an OWNER role except make a member an OWNER or delete the group.
                                             A group can have multiple MANAGER members.
                                - "MEMBER":  This role can subscribe to a group, view discussion archives, and view the group's membership list.
                                - "OWNER":   This role can send messages to the group, add or remove members, change member roles, change group's settings, and delete the group.
                                             An OWNER must be a member of the group. A group can have more than one OWNER.
            member_type (str):  The type of group member. (default "USER")
                                Acceptable values are:
                                - "CUSTOMER": The member represents all users in a domain. An email address is not returned and the ID returned is the customer ID.
                                - "EXTERNAL": The member is a user or group from outside the domain. (Not currently used)
                                - "GROUP":    The member is another group.
                                - "USER":     The member is a user.
            delivery_settings (str): Defines mail delivery preferences of member. This is only supported by create/update/get.
                                Acceptable values are:
                                - "ALL_MAIL": All messages, delivered as soon as they arrive.
                                - "DAILY":    No more than one message a day.
                                - "DIGEST":   Up to 25 messages bundled into a single message.
                                - "DISABLED": Remove subscription.
                                - "NONE":     No messages.


        Returns:
            dict: member
        """
        body = {
            "delivery_settings": delivery_settings,
            "role": member_role,
            "type": member_type,
            "email": member_email
        }
        return self.admin_directory.members().insert(groupKey=group_key, body=body).execute()

    def update_member(self, group_key, member_key, member_role=None, delivery_settings=None):
        """
        Update membership of a user in the specified group.

        Args:
            groupKey: string, Email or immutable ID of the group. If ID, it should match with id of group object (required)
            memberKey: string, Email or immutable ID of the user. If ID, it should match with id of member object (required)

        Returns:
            dict:
                { # JSON template for Member resource in Directory API.
                    "status": "A String", # Status of member (Immutable)
                    "kind": "admin#directory#member", # Kind of resource this is.
                    "delivery_settings": "A String", # Delivery settings of member
                    "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
                    "etag": "A String", # ETag of the resource.
                    "role": "A String", # Role of member
                    "type": "A String", # Type of member (Immutable)
                    "email": "A String", # Email of member (Read-only)
                }
        """

        member = self.get_member(group_key=group_key, member_key=member_key)

        if member_role is None:
            member_role = member["role"]

        if delivery_settings is None:
            delivery_settings = member["delivery_settings"]

        body = {
            "delivery_settings": delivery_settings,
            "role": member_role,
        }

        return self.admin_directory.members().patch(groupKey=group_key, memberKey=member_key, body=body).execute()

    def delete_member(self, group_key, member_key):
        """
        Delete a member from a group.

        Args:
            group_key (str):  Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID.
            member_key (str): Identifies the group member in the API request. A group member can be a user or another group.
                              The value can be the member's (group or user) primary email address, alias, or unique ID.
        """

        self.admin_directory.members().delete(
            groupKey=group_key,
            memberKey=member_key
        ).execute()

    def list_members(self, group_key):
        """
        Retrieve all members in a group.

        Args:
            group_key (str):  Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID.

        Returns:
            dict:
                { # JSON response template for List Members operation in Directory API.
                    # Token used to access next page of this result.
                    "nextPageToken": "A String",
                    # Kind of resource this is.
                    "kind": "admin#directory#members",
                    "etag": "A String", # ETag of the resource.
                    "members": [ # List of member objects.
                    { # JSON template for Member resource in Directory API.
                        "status": "A String", # Status of member (Immutable)
                        # Kind of resource this is.
                        "kind": "admin#directory#member",
                        "delivery_settings": "A String", # Delivery settings of member
                        # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
                        "id": "A String",
                        "etag": "A String", # ETag of the resource.
                        "role": "A String", # Role of member
                        "type": "A String", # Type of member (Immutable)
                        "email": "A String", # Email of member (Read-only)
                        },
                    ],
                }
        """

        return self.admin_directory.members().list(groupKey=group_key).execute()
