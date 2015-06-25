import Ember from 'ember';
import RefreshableRoute from '../../mixins/refreshable-route';

export default Ember.Route.extend(RefreshableRoute, {

    needs: ['test'],

    model: function() {
        return this.store.query('comment', {test_id: this.modelFor('test').id});
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('comments', model);
        controller.set('test', this.modelFor('test'));
        controller.createNewComment();
    }


});
