import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import InfinityRoute from '../../../mixins/infinity-route';
import ComplexModelRoute from '../../../mixins/complex-model-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, InfinityRoute, ComplexModelRoute, {

    model: function() {
	const parent = this.modelFor('session.test').test_model;
	return Ember.RSVP.hash({
	    errors: this.infinityModel('error', {
		test_id: parent.id,
		modelPath: 'errors',
	    }),
	});
    },

});
