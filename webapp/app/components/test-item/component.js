import Ember from 'ember';

export default Ember.Component.extend({
    attributeBindings: ['href'],
    tagName: 'a',
    classNames: ['item', 'test', 'clickable'],

    classNameBindings: ['status'],

    test: Ember.computed.oneWay('item'),

    status: function() {
        let status = this.get('test.status').toLowerCase();
        if (status === 'failure' || status === 'error') {
            status = 'failed';
        }
        return status;
    }.property('test.status'),

    is_running: Ember.computed.equal('status', 'running'),

    href: function() {
        return '/#/tests/' + this.get('test.id');
    }.property('test.id'),


});
