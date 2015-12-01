import Ember from 'ember';

export default Ember.Controller.extend({

    queryParams: ['page',
                  {
                      filter: {
                          scope: "controller"
                      }
                  }],

    page: 1,
    pages_total: null,
    filter: undefined,
    filter_config: null,

    get_new_filter_with: function(name, value) {
        let returned = this.get('decoded_filter');
        if (returned[name] === value) {
            delete returned[name];
        } else {
            returned[name] = value;
        }
        if (Ember.$.isEmptyObject(returned)) {
            return undefined;
        }
        return JSON.stringify(returned);
    },

    decoded_filter: function() {
        let returned = this.get('filter');
        if (returned === undefined) {
            returned = {};
        } else {
            returned = JSON.parse(returned);
        }
        return returned;
    }.property('filter'),


    actions: {
        goto_page: function(page) {
            this.set('page', page);
        },

        update_filter: function(name, value) {
            this.transitionToRoute({queryParams: {page: this.get('page'), filter: this.get_new_filter_with(name, value)}});
        },

    }
});
