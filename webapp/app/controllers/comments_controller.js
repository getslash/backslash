import Ember from 'ember';

export default Ember.Controller.extend({

    api: Ember.inject.service(),

    createNewComment: function() {
        this.set('new_comment', this.store.createRecord('comment', {edited: true}));
    },

    actions: {
        saveComment: function(comment) {
            let self = this;
            let params = this.getSaveCommentParams(comment);
            self.get('api').call('post_comment', params)
                .then(function() {
                    self.send('refreshRoute');
                });
        },

        deleteComment: function(comment) {
            let self = this;

            self.get('api').call('delete_comment', {comment_id: parseInt(comment.id)}).then(
                function() {
                    comment.set('deleted', true);
                });
        }
    }


});
