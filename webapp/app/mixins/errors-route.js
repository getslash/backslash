import Ember from 'ember';

import InfinityRoute from 'ember-infinity/mixins/route';


export default Ember.Mixin.create(InfinityRoute, {

    perPageParam: "page_size",
    pageParam: "page",
    totalPagesParam: "meta.pages_total",

    model: function() {
        const parent_model_name = this.get('parent_model_name');
        let parent = this.modelFor(parent_model_name);
        let query_params = {};
        if (parent_model_name === 'session') {
            query_params['session_id'] = parent.id;
        } else {
            query_params['test_id'] = parent.id;
        }

        query_params['modelPath'] = 'controller.errors';

        let props = {
            errors: this.infinityModel("error", query_params),
        };
        props[parent_model_name] = parent;

        if (parent_model_name === 'test') {
            props['session'] = this.store.find('session', parent.get('session_id'));
        }

        return Ember.RSVP.hash(props);

    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.setProperties(model);
    },

    renderTemplate: function() {
        this.render('errors');
    },

    afterModel(model) {
        if (model.errors.get('meta.total') === 1) {
          this.transitionTo(`${this.get('parent_model_name')}.single_error`, 1);
        }
    }


});
