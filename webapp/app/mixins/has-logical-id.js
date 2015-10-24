import DS from 'ember-data';
import Ember from 'ember';

export default Ember.Mixin.create({

    logical_id: DS.attr(),

    display_id: function() {
        let logical_id = this.get('logical_id');
        if (logical_id !== null) {
            return logical_id;
        }
        return this.get('id');
    }.property('logical_id')

});
