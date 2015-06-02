import DS from 'ember-data';

export default DS.Model.extend({

    start_time: DS.attr('number'),
    end_time: DS.attr('number'),
    duration: DS.attr('number'),
    status: DS.attr('string'),
    name: DS.attr('string'),

    is_success: function() {
        return (this.get('status') === 'SUCCESS');
    }.property('status'),

});
