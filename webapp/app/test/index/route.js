import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['test'],

    model: function() {
        return this.modelFor('test');
    }
});
