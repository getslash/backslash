import Ember from 'ember';

const _ALL_FILTERS = ['show_successful', 'show_unsuccessful', 'show_abandoned', 'show_skipped'];

export default Ember.Mixin.create({
    queryParams: _ALL_FILTERS,

    show_successful: true,
    show_unsuccessful: true,
    show_abandoned: true,
    show_skipped: true,

    reset_page: function() {
        this.set('page', 1);
    }.observes(..._ALL_FILTERS),


    filter_all_except(filter_name) {
        for (let name of this.get_filters()) {
            this.set('show_' + name, name === filter_name);
        }
    },

    filter_none() {
        for (let name of this.get_filters()) {
            this.set('show_' + name, true);
        }
    },

    get_filters() {
        let returned = [];

        for (let param of this.get('queryParams')) {
            if (param.startsWith && param.startsWith('show_')) {
                returned.push(param.substr(5));
            }
        }
        return returned;
    },

});
