import Ember from 'ember';
import RefreshableRoute from '../../mixins/refreshable-route';

export default Ember.Route.extend(RefreshableRoute, {

    needs: ['session'],

    model: function() {
        return this.store.find('comment', {session_id: this.modelFor('session').id});
    },

    setupController: function(controller, model) {
        this._super(controller, model);
        controller.set('comments', model);
        controller.set('session', this.modelFor('session'));
        controller.createNewComment();
    }

});
