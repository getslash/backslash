import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import StatusFilterableRoute from '../mixins/status-filterable/route';
import PaginatedFilteredRoute from '../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, StatusFilterableRoute, {

    title: 'Test Information',

    model(params) {
	let query_params = {
                info_id: params.id,
                page: params.page,
                page_size: params.page_size,
        };

        for (let key in params) {
            if (key.startsWith('show_')) {
                query_params[key] = params[key];
            }
        }


        return Ember.RSVP.hash({
            tests: this.store.query('test', query_params),
            test_info: this.store.find('test-info', params.id).then(o => o.getProperties(['file_name', 'class_name', 'name'])),
        });
    },

    setupController(controller, model) {
        controller.setProperties(model);
    },

    renderTemplate() {
	this._super(...arguments);
	this.render('filter-controls', {
	    into: 'test_info',
	    outlet: 'filter-controls',
	});
    },


});
