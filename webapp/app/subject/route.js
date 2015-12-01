import Ember from 'ember';

import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    model(params) {
        return Ember.RSVP.hash({
            subject: this.store.find('subject', params.name),
            sessions: this.store.query('session', {}),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    },

});
