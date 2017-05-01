class Capability(object):

    def enabled_for(self, user):
        raise NotImplementedError() # pragma: no cover

class RoleBasedCapability(Capability):

    def __init__(self, *roles):
        super(RoleBasedCapability, self).__init__()
        self.roles = roles

    def enabled_for(self, user):
        return any(user.has_role(role) for role in self.roles)

class AnyUser(Capability):

    def enabled_for(self, user):
        return user.is_authenticated


_MODERATORS = RoleBasedCapability('moderator', 'admin')
_ADMINS = RoleBasedCapability('admin')
_PROXIES = RoleBasedCapability('proxy')
_ALL = AnyUser()

CAPABILITIES = {
    'admin': _ADMINS,
    'archive_session': _MODERATORS,
    'comment_test': _ALL,
    'comment_session': _ALL,
    'edit_user_roles': _ADMINS,
}
