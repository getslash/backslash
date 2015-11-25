import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    model: function() {
        const session = this.modelFor('session');
        return Ember.RSVP.hash({
            session: session,
            warnings: this.store.query('warning', {session_id: session.id})
        });
    },

    setupController: function(controller, model) {
        controller.setProperties(model);
    }
});
