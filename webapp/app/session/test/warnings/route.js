import Ember from 'ember';
import BaseRoute from '../../../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import InfinityRoute from '../../../mixins/infinity-route';
import ComplexModelRoute from '../../../mixins/complex-model-route';

export default BaseRoute.extend(AuthenticatedRouteMixin, InfinityRoute, ComplexModelRoute, {

    model: function() {
	const parent = this.modelFor('session.test').test_model;
	return Ember.RSVP.hash({
	    warnings: this.infinityModel('warning', {
		test_id: parent.id,
		modelPath: 'controller.warnings',
	    }),
	});
    },

});
