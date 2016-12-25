import Ember from 'ember';

export default Ember.Component.extend({

    text: null,

    can_commit: Ember.computed.notEmpty('text'),

});
