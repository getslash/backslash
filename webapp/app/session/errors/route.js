import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import InfinityRoute from '../../mixins/infinity-route';
import ComplexModelRoute from '../../mixins/complex-model-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, InfinityRoute, ComplexModelRoute, {

    model: function() {
	const parent = this.modelFor('session').session_model;
	return Ember.RSVP.hash({
	    session: this.modelFor('session').session_model,
	    errors: this.infinityModel('error', {
		session_id: parent.id,
		modelPath: 'controller.errors',
	    }),
	});
    },

});
