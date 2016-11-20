import Ember from 'ember';

export default Ember.Component.extend({

    page: 1,
    has_next: false,

    paginated: function() {
        return this.get('pages_total') !== 1;
    }.property('pages_total'),

    
    has_prev: function() {
        return this.get('page') !== 1;
    }.property('page'),


    actions: {
        goto: function(page) {
            let self = this;
            let p = self.get('page');
            if (page === "next") {
                p = self.get('has_next')?(p + 1):p;
            } else if (page === "prev") {
                p = self.get('has_prev')?(p - 1):p;
            } else if (page === 'last') {
                p = self.get('pages_total');
            } else if (page === 'first') {
                p = 1;
            } else {
                p = page;
            }
            this.sendAction('goto_page', p);
        }
    }
});
