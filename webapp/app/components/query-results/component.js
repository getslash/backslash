import Ember from 'ember';

export default Ember.Component.extend({

    results: null,
    show_subjects: true,
    session_model: null,

    display: Ember.inject.service(),


    page: Ember.computed.oneWay('results.meta.page'),
    pages_total: Ember.computed.oneWay('results.meta.pages_total'),
    page_size: null,
    filter_config: Ember.computed.oneWay('results.meta.filter_config'),


    actions: {
        set_page_size(size) {
            this.set('page_size', size);
        },
    },
});
