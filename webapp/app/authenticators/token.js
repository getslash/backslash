import Base from 'simple-auth/authenticators/base';
import Ember from "ember";

export default Base.extend({
  restore: function(credentials) {
    return Ember.$.ajax({
      type: "POST",
      url: "/reauth",
      contentType : 'application/json',
      data: JSON.stringify(credentials)
    });
  },
  authenticate: function(credentials) {
    return Ember.$.ajax({
      type: "POST",
      url: "/login",
      contentType : 'application/json',
      data: JSON.stringify(credentials)
    });
  },
});
