import Ember from 'ember';

export default Ember.Route.extend({
    queryParams: {
        page: {
            refreshModel: true
        },
        filter: {
            refreshModel: true,
        }
    },

     setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('pages_total', model.get('meta.pages_total'));
        controller.set('filter_config', model.get('meta.filter_config'));
    },

    resetController: function (controller, isExiting) {
        if (isExiting) {
            controller.set('filter', undefined);
        }
    }



});
