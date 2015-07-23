import Ember from 'ember';

export default Ember.Route.extend({
    page: 1,
    pages_total: null,

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
        controller.set('pages_total', model.get('meta.pages_total'));
    },

    resetController: function (controller, isExiting) {
        if (isExiting) {
            controller.set('page', 1);
        }
    }
});
