import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
    user_id: DS.attr('number'),
    comment: DS.attr(),
    timestamp: DS.attr(),
    edited: DS.attr('boolean'),
    user_email: DS.attr(),

    can: DS.attr(),

    has_text: function() {
        return Ember.$.trim(this.get('comment')) !== '';
    }.property('comment')
});
