import Ember from 'ember';

export default Ember.Route.extend({
    needs: ['session'],

    model: function() {
        return this.store.query('activity', {session_id: this.modelFor('session').id});
    },

    actions: {
        refresh: function() {
            this.refresh();
        }
    }
});
