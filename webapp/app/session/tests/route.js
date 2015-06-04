import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['session'],

    model: function() {
        return this.store.find('test', {session_id: this.modelFor('session').id});
    }
});
