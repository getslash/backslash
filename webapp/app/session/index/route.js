import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['session'],

    model: function() {
        return Ember.$.ajax({
            type: 'POST',
            url: '/api/get_metadata',
            contentType: 'application/json',
            data: JSON.stringify({
                entity_type: 'session',
                entity_id: parseInt(this.modelFor('session').id)
            })
        });
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('metadata', model.result);
        controller.set('session', this.modelFor('session'));
    }
});
