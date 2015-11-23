import DS from 'ember-data';
import Ember from 'ember';

export default DS.Model.extend({
    email: DS.attr(),
    user_roles: DS.attr(),

    display_name: Ember.computed.oneWay('email'),

    last_activity: DS.attr()

});
