import Ember from 'ember';

export default Ember.Component.extend({

    additional: {},
    metadata: {},

    all_metadata: function() {
        let returned = {};

        [this.get('additional'), this.get('metadata')].forEach(function(obj) {
            for (var attrname in obj) {
                returned[attrname] = obj[attrname];
            }
        });
        console.log('all metadata:', returned);
        return returned;
    }.property('additional', 'metadata')

});
