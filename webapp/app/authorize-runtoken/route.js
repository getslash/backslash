import $ from 'jquery';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default Route.extend(AuthenticatedRouteMixin, {
  model: function(params) {
    return $.ajax({
      type: "POST",
      url: "/runtoken/request/" + params.requestid + "/complete",
      contentType: "application/json",
      data: JSON.stringify({})
    });
  }
});
