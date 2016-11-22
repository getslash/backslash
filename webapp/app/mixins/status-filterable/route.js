import Ember from 'ember';

export default Ember.Mixin.create({
    queryParams: {
        page: {
            refreshModel: true
        },
	page_size: {
	    refreshModel: true,
	},
        filter: {
            refreshModel: true,
        },
        show_successful: {
            refreshModel: true,
        },
        show_unsuccessful: {
            refreshModel: true,
        },
        show_abandoned: {
            refreshModel: true,
        },
        show_skipped: {
            refreshModel: true,
        },
    },

    transfer_filter_params(from_params, to_params) {
        let query_params = this.get('queryParams');
        for (let key in query_params) {
            if (key.startsWith('show_')) {
                to_params[key] = from_params[key];
            }
        }
    },
});
