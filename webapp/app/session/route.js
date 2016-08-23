import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ScrollToTopMixin from '../mixins/scroll-top';
import PollingRoute from '../mixins/polling-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, ScrollToTopMixin, PollingRoute, {

    api: Ember.inject.service(),
    title: 'Session Tests',

    model(params) {
	let self = this;
	return self.store.find('session', params.id).then(function(session) {
 	    return Ember.RSVP.hash({
		'session_model': session,
		'user': self.store.find('user', session.get('user_id')),
	    });
        });
    },

    should_auto_refresh: function() {
	const end_time = this.modelFor('session').session_model.get('end_time');
	return end_time === null;
    },

    setupController: function(controller, model) {
      this._super(controller, model);
      controller.setProperties(model);
    }


});
