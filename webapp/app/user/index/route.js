import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['user'],
    
    model: function() {
        return this.modelFor('user');
    }
});
