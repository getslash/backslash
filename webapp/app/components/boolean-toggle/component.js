import Ember from 'ember';

export default Ember.Component.extend({

    enabled: true,

    actions: {
        toggle: function() {
            this.sendAction();
        }
    }
});
