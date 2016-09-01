import Ember from 'ember';

import PaginatedFilteredRoute from '../routes/paginated_filtered_route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import PollingRoute from '../mixins/polling-route';
import ScrollToTopMixin from '../mixins/scroll-top';
import StatusFilterableRoute from '../mixins/status-filterable/route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, PollingRoute, ScrollToTopMixin, StatusFilterableRoute, {

    titleToken: 'Sessions',

    user_prefs: Ember.inject.service(),

    model(params) {
        let query_params = {page: params.page, filter: params.filter, page_size: params.page_size};
        this.transfer_filter_params(params, query_params);

        let user_id = this.get_user_id_parameter();

        if (user_id !== undefined) {
            query_params.user_id = user_id;
        }
	return Ember.RSVP.hash({
	    sessions: this.store.query('session', query_params),
	    prefs: this.get('user_prefs').get_all(),
	});
    },

    setupController(controller, model) {
        controller.set('sessions', model.sessions);
    },

    get_user_id_parameter: function() {
        return undefined;
    },

    renderTemplate() {
	this._super(...arguments);
	this.render('filter-controls', {
	    into: 'sessions',
	    outlet: 'filter-controls',
	});
    },


});
