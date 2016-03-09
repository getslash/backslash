import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['query-result', 'clickable'],
    classNameBindings: ['result.investigated:investigated', 'result.is_abandoned:abandoned', 'result_type'],
    result: null,

    result_type: Ember.computed.oneWay('result.type'),

    typename: Ember.computed.oneWay('result.type'),

    click: function() {
        this.sendAction('route_to', this.get('typename'), this.get('result.display_id'));
    },


});
