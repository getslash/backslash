import Ember from 'ember';

export default Ember.Mixin.create({
    model() {
        let parent = this.get_parent();

        let query_params = {page_size: 200};
        query_params[parent.constructor.modelName + '_id'] = parent.get('id');
        return Ember.RSVP.hash({
            parent: parent,
            comments: this.store.query('comment', query_params),
        });

    },

    setupController(controller, model) {
        controller.setProperties(model);
    },


});
