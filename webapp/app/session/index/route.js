import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import RefreshableRouteMixin from '../../mixins/refreshable-route';
import PaginatedFilteredRoute from '../../routes/paginated_filtered_route';

export default PaginatedFilteredRoute.extend(AuthenticatedRouteMixin, RefreshableRouteMixin, {

    title: 'Session Details',

    model: function(params) {
        let session = this.modelFor('session');
        const session_id = parseInt(session.id);
        return Ember.RSVP.hash({
            'metadata': this.api.call('get_metadata', {
                entity_type: 'session',
                entity_id: session_id
            }).then(r => r.result),

            'tests': this.store.query('test', {session_id: session_id, page: params.page, filter: params.filter}),
            'history': [
            ]
        });
    },

    setupController: function(controller, model) {
      this._super(controller, model);
      controller.setProperties(model);
      controller.set('session_model', this.modelFor('session'));
    }

});
