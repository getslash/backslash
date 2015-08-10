import DS from 'ember-data';

export default DS.Model.extend({
    message: DS.attr(),
    timestamp: DS.attr(),
    user_email: DS.attr(),
    what: DS.attr()

});
