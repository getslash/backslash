import Ember from 'ember';
import RefreshableRouteMixin from '../../mixins/refreshable-route';

export default Ember.Route.extend(RefreshableRouteMixin, {
    needs: ['session'],

    model: function() {
        return this.store.query('activity', {session_id: this.modelFor('session').id});
    },
});
