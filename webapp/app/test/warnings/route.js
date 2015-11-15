import Ember from 'ember';

export default Ember.Route.extend({
    model: function() {
        const test = this.modelFor('test');
        return Ember.RSVP.hash({
            test: test,
            session: this.store.find('session', test.get('session_id')),
            warnings: this.store.query('warning', {test_id: test.id})
        });
    },

    setupController: function(controller, model) {
        controller.setProperties(model);
    }


});
