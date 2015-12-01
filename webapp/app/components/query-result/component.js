import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['container-fluid', 'query-result', 'test', 'clickable'],
    classNameBindings: ['result.investigated:investigated', 'result.is_abandoned:abandoned'],
    result: null,

    typename: Ember.computed.oneWay('result.type'),

    click: function() {
        this.sendAction('route_to', this.get('typename'), this.get('result.display_id'));
    },


});
