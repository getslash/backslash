import Ember from 'ember';

export default Ember.Component.extend({

    results: null,
    humanize_times: true,

    page: Ember.computed.oneWay('results.meta.page'),
    pages_total: Ember.computed.oneWay('results.meta.pages_total'),
    filter_config: Ember.computed.oneWay('results.meta.filter_config'),

});
