import BaseRoute from '../routes/base';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default BaseRoute.extend(AuthenticatedRouteMixin, {
  beforeModel: function() {
    this.transitionTo('sessions',{queryParams: {page: 1, filter: undefined, show_archived:false}});
  }
});
