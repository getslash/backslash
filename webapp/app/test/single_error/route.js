import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    model: function(params) {

        let test = this.modelFor('test');

        return Ember.RSVP.hash({
            'error': this.store.find('error', params.error_id),
            'test': test,
            'session': this.store.find('session', test.get('session_id'))
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);

    },

    renderTemplate: function() {
        this.render('single_error');
    }

});
