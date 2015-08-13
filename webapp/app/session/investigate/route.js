import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['session'],

    model: function() {
        return this.modelFor('session');
    }
});
