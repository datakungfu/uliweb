from rbac import *
from uliweb.core.dispatch import bind

@bind('prepare_default_env')
def prepare_default_env(sender, env):
    from rbac import has_permission, has_role
    env['has_permission'] = has_permission
    env['has_role'] = has_role
    
@bind('after_init_apps')
def startup(sender):
    from uliweb import settings
    from rbac import register_role_method
    
    if 'ROLES' in settings:
        for k, v in settings.get_var('ROLES', {}).iteritems():
            if isinstance(v, (list, tuple)) and len(v) > 1:
                method = v[1]
                if method:
                    register_role_method(k, method)
