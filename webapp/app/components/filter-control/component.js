import Ember from 'ember';

export default Ember.Component.extend({

    filter_config: [],

    actions: {
        update_filter(name, value) {
            this.sendAction('update_filter', name, value);
        },
    }

});
