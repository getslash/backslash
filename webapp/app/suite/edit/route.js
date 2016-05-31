import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ComplexModelRoute from '../../mixins/complex-model-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, ComplexModelRoute, {

    titleToken: 'Edit',

    model() {
	let suite = this.modelFor('suite');
	return Ember.RSVP.hash({
	    suite: suite,
	    items: this.api.call('get_suite_items', {suite_id: parseInt(suite.id)}),
	});

    },
});
