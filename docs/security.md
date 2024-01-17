# LabKey Security API Overview

Manage user permissions. Also use impersonation and who_am_i for troubleshooting or permissions validation.

LabKey Server has a group- & role-based security model that operates on a per-container basis primarily. This means that each user of the system belongs to one or more security groups, and can be assigned different roles (combinations of permissions) related to resources the system.

For more info about LabKey security configuration see here, https://www.labkey.org/Documentation/wiki-page.view?name=security.

### LabKey Security API Methods

To use the security API methods, you must first instantiate an APIWrapper object. See the APIWrapper docs page to learn more about how to properly do so, accounting for your LabKey Server's configuration details.

**activate_users**


**add_to_group**


**add_to_role**


**create_user**


**deactivate_users**


**delete_users**


**get_roles**


**get_user_by_email**


**list_groups**


**remove_from_group**


**remove_from_role**


**reset_password**


**impersonate_user**


**stop_impersonating**


**who_am_i**


