import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['activity-icon'],
    classNameBindings: ['activity_icon_class'],

    activity_icon_class: Ember.computed.oneWay('item.action'),

    icon: function() {
        let action = this.get('item.action');

        switch (action) {
            case 'comment':
                return 'comment';
            default:
                return 'question';
        }
    }.property('item.action'),

    item: null
});
