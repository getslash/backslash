import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

import PaginatedFilteredRoute from '../../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {
    model(params) {
        const test = this.modelFor('test');
        return Ember.RSVP.hash({
            test: test,
            session: this.store.find('session', test.get('session_id')),
            warnings: this.store.query('warning', {test_id: test.id, page: params.page})
        });
    },

    setupController: function(controller, model) {
        controller.setProperties(model);
    }


});
