import Ember from 'ember';

export default Ember.Controller.extend({

    queryParams: ['sort'],

    sort: 'last_activity',

    sort_options: ['last_activity', 'name'].sort(),

});
