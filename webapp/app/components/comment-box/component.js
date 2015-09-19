import Ember from 'ember';

export default Ember.Component.extend({
    comment: null,

    session: Ember.inject.service(),

    defineProperties: function() {
        Ember.defineProperty(this, 'commentEdited', Ember.computed.alias('comment.edited'));
  }.on('init'),


    email: function() {
        if (this.get('commentEdited')) {
            return this.get('session.data.authenticated.user_info.email');
        }
        return this.get('comment').get('user_email');
    }.property('commentEdited'),

    mine: function() {
        return this.get('comment.user_email') === this.get('session.data.authenticated.user_info.email');
    }.property(),

    actions: {

        delete: function() {
            let self = this;
            if (window.confirm('Are you sure?')) {
                self.sendAction('deleteComment', this.get('comment'));
            }
        },

        save: function() {
            this.sendAction('saveComment', this.get('comment'));
        }
    }
});
