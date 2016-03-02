class Capability(object):

    def enabled_for(self, user):
        raise NotImplementedError() # pragma: no cover

class RoleBasedCapability(Capability):

    def __init__(self, role):
        super(RoleBasedCapability, self).__init__()
        self.role = role

    def enabled_for(self, user):
        return user.has_role(self.role)

class AnyUser(Capability):

    def enabled_for(self, user):
        return user.is_authenticated


_MODERATORS = RoleBasedCapability('moderator')
_ADMINS = RoleBasedCapability('admin')
_PROXIES = RoleBasedCapability('proxy')
_ALL = AnyUser()

CAPABILITIES = {
    'comment_test': _ALL,
    'comment_session': _ALL,
}
