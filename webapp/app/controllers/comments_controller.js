import Ember from 'ember';

export default Ember.Controller.extend({
    createNewComment: function() {
        this.set('new_comment', this.store.createRecord('comment', {edited: true}));
    },

    actions: {
        saveComment: function(comment) {
            let self = this;
            let params = this.getSaveCommentParams(comment);
            self.api.call('post_comment', params)
                .then(function() {
                    self.send('refreshRoute');
                });
        }
    }


});
