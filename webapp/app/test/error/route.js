import Ember from 'ember';

export default Ember.Route.extend({

    model: function(params) {

        return this.store.find('error', params.error_id);
    },


    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('error', model);
        controller.set('test', this.controllerFor('test').get('test'));
        
    },

    renderTemplate: function() {
        this.render('error');
    }

});
