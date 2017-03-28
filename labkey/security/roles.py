from abc import ABC, abstractmethod


# using abstract class instead of Enum since Roles may need to be extended
class Role(ABC):
    @abstractmethod
    def get_unique_name(self): pass


class SiteAdminRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.siteAdminRole'


class ProjectAdminRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.ProjectAdminRole'


class FolderAdminRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.FolderAdminRole'


class EditorRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.EditorRole'


class AuthorRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.AuthorRole'


class ReaderRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.ReaderRole'


class RestrictedReaderRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.RestrictedReaderRole'


class SubmitterRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.SubmitterRole'


class NoPermissionsRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.NoPermissionsRole'


class OwnerRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.OwnerRole'


class DeveloperRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.DeveloperRole'


class TroubleshooterRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.TroubleshooterRole'


class SeeEmailAddressesRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.SeeEmailAddressesRole'


class CanSeeAuditLogRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.CanSeeAuditLogRole'


class EmailNonUsersRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.EmailNonUsersRole'


class SharedViewEditorRole(Role):
    def get_unique_name(self):
        return 'org.labkey.api.security.roles.SharedViewEditorRole'


def lookup_roles(role_name):
        roles = {
            'SiteAdminRole': SiteAdminRole(),
            'ProjectAdminRole': ProjectAdminRole(),
            'FolderAdminRole': FolderAdminRole(),
            'EditorRole': EditorRole(),
            'AuthorRole': AuthorRole(),
            'ReaderRole': ReaderRole(),
            'RestrictedReaderRole': RestrictedReaderRole(),
            'SubmitterRole': SubmitterRole(),
            'NoPermissionsRole': NoPermissionsRole(),
            'OwnerRole': OwnerRole(),
            'DeveloperRole': DeveloperRole(),
            'TroubleshooterRole': TroubleshooterRole(),
            'SeeEmailAddressesRole': SeeEmailAddressesRole(),
            'CanSeeAuditLogRole': CanSeeAuditLogRole(),
            'EmailNonUsersRole': EmailNonUsersRole(),
            'SharedViewEditorRole': SharedViewEditorRole()
        }

        if role_name in roles:
            return roles[role_name]
        else:
            return None
