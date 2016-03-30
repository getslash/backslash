import Ember from 'ember';

export default Ember.Component.extend({

    value: null,
    options: [],

    dropdown_id: 'dropdown1',

    actions: {
        select(item) {
            this.set('value', item);
        },
    },

});
