import { hash } from 'rsvp';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import ComplexModelRoute from '../../mixins/complex-model-route';
import PollingRoute from "../../mixins/polling-route";

export default Route.extend(AuthenticatedRouteMixin, ComplexModelRoute, PollingRoute, {

    model: function() {
      let parent_logical_id = this.modelFor('session').session_model.get('logical_id');
      let query_params = {parent_logical_id: parent_logical_id};
      return hash({
        children: this.store.query('session', query_params),
      });
    },
    should_auto_refresh: function() {
      const end_time = this.modelFor("session").session_model.get("end_time");
      return end_time === null;
    },
});
