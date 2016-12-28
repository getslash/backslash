import Ember from 'ember';

import RefreshableRouteMixin from '../../mixins/refreshable-route';
import CommentsRouteMixin from '../../mixins/comments-route';

export default Ember.Route.extend(RefreshableRouteMixin, CommentsRouteMixin, {

    get_parent() {
        return this.modelFor('session').session_model;
    },
});
