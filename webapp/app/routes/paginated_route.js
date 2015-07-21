import Ember from 'ember';

export default Ember.Route.extend({
    page: 1,

    queryParams: {
        page: {
            refreshModel: true
        }
    },

    parsePage: function(params) {
        this.set('page', params.page?parseInt(params.page):1);
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('page', this.get('page'));
    },

    resetController: function (controller, isExiting) {
        if (isExiting) {
            controller.set('page', 1);
        }
    }
});
