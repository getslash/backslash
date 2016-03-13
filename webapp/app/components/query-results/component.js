import Ember from 'ember';

export default Ember.Component.extend({

    results: null,

    page: Ember.computed.oneWay('results.meta.page'),
    pages_total: Ember.computed.oneWay('results.meta.pages_total'),
    num_visible: Ember.computed.oneWay('results.meta.page_size'),
    filter_config: Ember.computed.oneWay('results.meta.filter_config'),

});
