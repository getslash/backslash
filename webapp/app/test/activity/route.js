import Ember from 'ember';

export default Ember.Route.extend({
    needs: ['test'],

    model: function() {
        return this.store.query('activity', {test_id: this.modelFor('test').id});
    }
});
