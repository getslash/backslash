import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  model: function(params) {
    return Ember.$.ajax({
      type: "POST",
      url: "/runtoken/request/" + params.requestid + "/complete",
      contentType: "application/json",
      data: JSON.stringify({})
    });
  }
});
