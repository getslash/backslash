import Ember from 'ember';

import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ScrollToTopMixin from '../mixins/scroll-top';
import StatusFilterableRoute from '../mixins/status-filterable/route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, ScrollToTopMixin, StatusFilterableRoute, {

    titleToken(model) {
        return model.subject.get('name');
    },

    model(params) {
        let query_params = {
            subject_name: params.name,
            page: params.page,
        };
        this.transfer_filter_params(params, query_params);
        return Ember.RSVP.hash({
            subject: this.store.find('subject', params.name),
            sessions: this.store.query('session', query_params),
        });
    },

    setupController(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    },

});
