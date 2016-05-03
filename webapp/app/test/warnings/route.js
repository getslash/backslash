import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ErrorsWarningsRouteMixin from '../../mixins/errors-warnings-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, ErrorsWarningsRouteMixin, {
    parent_model_name: 'test',
    type: 'warning',
});
