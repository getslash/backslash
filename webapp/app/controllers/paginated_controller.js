import Ember from 'ember';

export default Ember.Controller.extend({

    has_prev_page: function() {
        return this.get('page') > 1;
    }.property('page'),

    has_next_page: true,

    queryParams: ['page'],

    actions: {
        next_page: function() {
            this.transitionToRoute({queryParams: {page: this.get('page') + 1}});
        },
        prev_page: function() {
            this.transitionToRoute({queryParams: {page: this.get('page') - 1}});
        }

    }
});
