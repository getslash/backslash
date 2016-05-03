import BaseRoute from '../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ErrorsRouteMixin from '../../mixins/errors-route';

export default BaseRoute.extend(AuthenticatedRouteMixin, ErrorsRouteMixin, {
    parent_model_name: 'session',
});
