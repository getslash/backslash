import Route from '@ember/routing/route';

import RefreshableRouteMixin from "../../../mixins/refreshable-route";
import CommentsRouteMixin from "../../../mixins/comments-route";

export default Route.extend(RefreshableRouteMixin, CommentsRouteMixin, {
  get_parent() {
    return this.modelFor("session.test").test_model;
  }
});
