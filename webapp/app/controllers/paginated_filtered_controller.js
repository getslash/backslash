import Ember from 'ember';

export default Ember.Controller.extend({

    queryParams: ['page', 'page_size',
                  {
                      filter: {
                          scope: "controller"
                      }
                  }],

    page: 1,
    page_size: 25,

    filter: undefined,
    collection: null,

    check_paging: function() {
        let self = this;
        Ember.run.later(function() {
            let page = self.get('page');
            let pages_total = self.get('collection.meta.pages_total');
            if (page > pages_total) {
                self.set('page', pages_total);
            }
            if (!page) {
                self.set('page', 1);
            }
        });
    }.observes('page', 'collection.meta.pages_total'),

    filter_config: function() {

        if (!this.get('collection')) {
            console.warn('Collection is unexpectedly null on ', this);
        }

        let raw = this.get('collection.meta.filter_config'), returned = {};

        if (raw === undefined) {
            return null;
        }

        raw.map(function(f) {
            returned[f.name] = f;
        });

        return returned;

    }.property('collection'),

    get_new_filter_with: function(name, value) {
        let returned = this.get('decoded_filter');
        if (returned[name] === value || value === this.get('filter_config.' + name + '.default')) {
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
        update_filter: function(name, value) {
            this.transitionToRoute({queryParams: {page: this.get('page'), filter: this.get_new_filter_with(name, value)}});
        },

    }
});
