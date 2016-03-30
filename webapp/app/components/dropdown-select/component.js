import Ember from 'ember';

export default Ember.Component.extend({

    value: null,
    title: null,
    options: [],


    actions: {
        select(item) {
            this.set('value', item);
        },
    },

});
