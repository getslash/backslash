import Ember from 'ember';

export default Ember.Component.extend({
    classNames: ['container', 'activity-timeline'],
    parent: null,
    items: [],

    new_comment: "",
    commenting: false,


    post_new_comment: function() {
        let self = this;
        let params = this.get_comment_params();
        self.api.call('post_comment', params)
            .then(function() {
                self.sendAction('comment_added');
            });
    },

    get_comment_params: function() {
        let returned = {
            comment: this.get('new_comment')
        };

        returned[this.get('parent.type') + '_id'] = parseInt(this.get('parent.id'));
        return returned;
    },


    actions: {

        start_commenting: function() {
            this.set('commenting', true);
        },

        finish_commenting: function() {
            this.post_new_comment();
            this.set('commenting', false);
        },

        cancel_commenting: function() {
            this.set('new_comment', '');
            this.set('commenting', false);
        }

    }
});
