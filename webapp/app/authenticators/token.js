import $ from 'jquery';
import Base from "ember-simple-auth/authenticators/base";

export default Base.extend({
  restore: function(credentials) {
    return $.ajax({
      type: "POST",
      url: "/reauth",
      contentType: "application/json",
      data: JSON.stringify(credentials)
    });
  },
  authenticate: function(credentials) {
    return $.ajax({
      type: "POST",
      url: "/login",
      contentType: "application/json",
      data: JSON.stringify(credentials)
    });
  }
});
