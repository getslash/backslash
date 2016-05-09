import BaseRoute from '../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ErrorsWarningsRouteMixin from '../../mixins/errors-warnings-route';

export default BaseRoute.extend(AuthenticatedRouteMixin, ErrorsWarningsRouteMixin, {
    parent_model_name: 'session',
});
