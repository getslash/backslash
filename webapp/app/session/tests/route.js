import Ember from 'ember';

export default Ember.Route.extend({

    needs: ['session'],

    model: function() {
        return this.store.query('test', {session_id: this.modelFor('session').id});
    }
});
