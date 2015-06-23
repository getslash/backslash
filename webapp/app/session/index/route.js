import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['session'],

    model: function() {
        return this.api.call('get_metadata', {
            entity_type: 'session',
            entity_id: parseInt(this.modelFor('session').id)
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('metadata', model.result);
        controller.set('session', this.modelFor('session'));
    }
});
