import Ember from 'ember';

export default Ember.Mixin.create({
    queryParams: ['humanize_times', 'show_successful', 'show_unsuccessful', 'show_abandoned', 'show_skipped'],

    humanize_times: true,
    show_successful: true,
    show_unsuccessful: true,
    show_abandoned: true,
    show_skipped: true,


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
