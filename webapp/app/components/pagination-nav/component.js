import Ember from 'ember';

export default Ember.Component.extend({

    page: 1,
    pages_total: null,

    num_visible: 10,

    paginated: function() {
        return this.get('pages_total') !== 1;
    }.property('pages_total'),

    has_next: function() {
        return this.get('page') !== this.get('pages_total');
    }.property('page', 'pages_total'),

    has_prev: function() {
        return this.get('page') !== 1;
    }.property('page', 'pages_total'),


    pages: function() {
        let returned = [];

        for (var i = this.get('start_number'); i <= this.get('end_number'); ++i) {
            returned.push({number: i, active: this.get('page') === i});
        }
        return returned;
    }.property('page', 'pages_total'),

    start_number: function() {
        let page = this.get('page');
        let num_visible = this.get('num_visible');
        if (page % num_visible === 0) {
            return page;
        }
        return ((Math.ceil(page / num_visible) - 1) * num_visible) + 1;
    }.property('page'),

    end_number: function() {
        let returned = this.get('start_number') + this.get('num_visible') - 1;
        if (returned > this.get('pages_total')) {
            returned = this.get('pages_total');
        }
        return returned;
    }.property('page', 'pages_total'),



    actions: {
        goto: function(page) {
            console.log('Going to page', page);
            let self = this;
            let p = self.get('page');
            if (page === "next") {
                p = self.get('has_next')?(p + 1):p;
            } else if (page === "prev") {
                p = self.get('has_prev')?(p - 1):p;
            } else {
                p = page;
            }
            this.sendAction('goto_page', p);
        }
    }
});
