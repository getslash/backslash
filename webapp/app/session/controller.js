import Ember from 'ember';

export default Ember.Controller.extend({
    current_test: null,
    test_filters: null,

    display: Ember.inject.service(),

});
