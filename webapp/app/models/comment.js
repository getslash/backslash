import DS from 'ember-data';

export default DS.Model.extend({
    user_id: DS.attr('number'),
    comment: DS.attr(),
    timestamp: DS.attr(),
    edited: DS.attr('boolean'),
    user_email: DS.attr()
});
