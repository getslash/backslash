import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import RefreshableRouteMixin from '../../mixins/refreshable-route';
import StatusFilterableRoute from '../../mixins/status-filterable/route';

export default Ember.Route.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, StatusFilterableRoute, {

    title: 'Session',
    queryParams: {
        show_planned: {
            refreshModel: true
        },
    },

    model: function(params) {
        let session = this.modelFor('session').session_model;
        const session_id = parseInt(session.id);

        let query_params = {
                session_id: session_id,
                page: params.page,
                page_size: params.page_size,
        };

        let filters = {};
        for (let key in params) {
            if (key.startsWith('show_')) {
                filters[key] = query_params[key] = params[key];
            }
        }

	return Ember.RSVP.hash({
	    session_model: session,
	    tests: this.store.query('test', query_params),
            filters: filters,
	});

    },

    renderTemplate() {
	this._super(...arguments);
	this.render('filter-controls', {
	    into: 'session',
	    outlet: 'filter-controls',
	});
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        let parent_controller = this.controllerFor('session');
        parent_controller.set('test_filters', model.filters);
        controller.setProperties(model);
    }

});
