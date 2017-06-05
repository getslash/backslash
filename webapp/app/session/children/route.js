import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ComplexModelRoute from '../../mixins/complex-model-route';

export default Ember.Route.extend(AuthenticatedRouteMixin, ComplexModelRoute, {

    model: function() {
      let parent_logical_id = this.modelFor('session').session_model.get('logical_id');
      let query_params = {parent_logical_id: parent_logical_id};
      return Ember.RSVP.hash({
        children: this.store.query('session', query_params),
      });
    },
});
