import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['test'],

    model: function() {

        return this.store.find('error', {test_id: this.modelFor('test').id});
    }
});
