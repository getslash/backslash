import Ember from 'ember';

import InfinityRoute from 'ember-infinity/mixins/route';


export default Ember.Mixin.create(InfinityRoute, {

    perPageParam: "page_size",
    pageParam: "page",
    totalPagesParam: "meta.pages_total",
    type: 'error',

    model: function() {
        const parent_model_name = this.get('parent_model_name');
        let parent = this.modelFor(parent_model_name);
        let query_params = {};
        if (parent_model_name === 'session') {
            query_params['session_id'] = parent.id;
        } else {
            query_params['test_id'] = parent.id;
        }

        query_params['modelPath'] = `controller.${this.get('type').pluralize()}`;

        let props = {};
        props[this.get('type').pluralize()] = this.infinityModel(this.get('type'), query_params);

        props['single_error_route'] = `${parent_model_name}.single_error`;
        props['parent_id'] = parent.get('display_id');

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
        this.render(this.get('type').pluralize());
    },

    afterModel(model) {

        if (this.get('type') === 'error' && model.errors.get('meta.total') === 1) {
          this.transitionTo(`${this.get('parent_model_name')}.single_error`, 1);
        }
    }


});
