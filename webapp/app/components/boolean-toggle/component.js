import Ember from 'ember';

export default Ember.Component.extend({

    actions: {
        toggle: function() {
            this.sendAction();
        }
    }
});
