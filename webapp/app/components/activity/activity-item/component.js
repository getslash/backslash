import Ember from 'ember';

export default Ember.Component.extend({

    item: null,
    parent: null,

    action_message: function() {

        return this.get('action_info.message').replace('%s', this.get('parent.type'));

    }.property('action_info'),

    action_info: function() {

        switch (this.get('item.action')) {
        case 'commented':
            return {
                icon: 'comment',
                message: 'commented on this %s'
            };

        case 'archived':
            return {
                icon: 'archive',
                message: 'archived this %s'
            };

        case 'unarchived':
            return {
                icon: 'archive',
                message: 'unarchived this %s'
            };

        case 'investigated':
            return {
                icon: 'check',
                message: 'marked this %s as investigated'
            };


        case 'uninvestigated':
            return {
                icon: 'times',
                message: 'marked this %s as not investigated'
            };


        default:
            return {
                icon: 'question',
                message: ''
            };
        }

    }.property('item.action')



});
