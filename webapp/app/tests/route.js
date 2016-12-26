import Ember from 'ember';

import ComplexModelRoute from '../mixins/complex-model-route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, ComplexModelRoute, {

    titleToken: 'Tests',

    queryParams: {
	search: {
	    replace: true,
	    refreshModel: true,
	},
	page: {
	    refreshModel: true,
	},
	page_size: {
	    refreshModel: true,
	},
    },

    model(params) {
	let query = {page: params.page, page_size: params.page_size};
	if (params.search) {
	    query.search = params.search;
	}
	return this.store.query('test', query).then(
	    function(tests) {
		return {tests: tests, error: null};
	    }
	).catch(
	    function(exception) {
		let message = null;
		exception.errors.forEach(function(e) {
		    message = e.detail;
		});

		if (message) {
		    return {error: message};
		}
		throw exception; // reraise
	    }
	);
    },

});
