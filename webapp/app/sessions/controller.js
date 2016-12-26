import Ember from 'ember';

import config from '../config/environment';


export default Ember.Controller.extend({

    available_page_sizes: config.APP.available_page_sizes,
    page_size: config.APP.default_page_size,

    collection: Ember.computed.oneWay('sessions'),

    display: Ember.inject.service(),

    entered_search: Ember.computed.oneWay('search'),

    queryParams: ['search', 'page', 'page_size'],

    search: '',

    actions: {
        search() {
            this.set('page', 1);
            this.set('search', this.get('entered_search'));
        },
    },


});
