import Ember from 'ember';

export default Ember.Mixin.create({

    state: Ember.inject.service(),

    actions: {

        loading: function(transition) {
            let state = this.get('state');
            state.set('loading', true);
            transition.promise.finally(function() {
                state.set('loading', false);
            });
        },
    },

});
