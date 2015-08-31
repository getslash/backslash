import Ember from 'ember';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Controller.extend(UnauthenticatedRouteMixin, {
  canSubmit: true,
  emailValid: function() {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(this.get("email"));
  }.property("email"),

  actions: {
    login: function() {
      if (!this.get("canSubmit")) {
        return;
      }

      if (!this.get("emailValid")) {
        this.set("errors", "Invalid email address");
        Ember.$("#email").focus();
        return;
      }

      if (!this.get("password")) {
        this.set("errors", "Password cannot be empty");
        Ember.$("#password").focus();
        return;
      }

      this.set("canSubmit", false);

      var self = this;
      var credentials = {
        email: this.get('email'),
        password: this.get('password')
      };
      this.get('session').authenticate('authenticator:token', credentials)
      .finally(function() {
        self.set("canSubmit", true);
      })
      .then(
        function(data) {
            return data;
        },
        function(reason) {
          var error = reason.statusText;
          if (reason.status === 401) {
            error = "Invalid username or password";
          }

          self.set("errors", error);
        });
    }
  }
});
