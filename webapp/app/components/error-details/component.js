import Ember from 'ember';

export default Ember.Component.extend({

    error: null,
    expanded: false,

    click: function() {
        this.set('expanded', !this.get('expanded'));
    }

});
