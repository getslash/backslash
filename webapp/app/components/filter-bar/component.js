import Ember from 'ember';

export default Ember.Component.extend({

    filter_config: [],

    actions: {
        filter: function(name, value) {
            this.sendAction('filter_action', name, value);
        }
    }

});
