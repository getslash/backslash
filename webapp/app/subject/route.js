import Ember from 'ember';

import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, {

    titleToken(model) {
        return model.subject.get('name');
    },

    model(params) {
        return Ember.RSVP.hash({
            subject: this.store.find('subject', params.name),
            sessions: this.store.query('session', {
                subject_name: params.name,
                page: params.page,
                filter: params.filter
            }),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    },

});
