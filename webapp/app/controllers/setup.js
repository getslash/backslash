import Ember from 'ember';

export default Ember.Controller.extend({
  errors: "",
  canSubmit: true,

  emailValid: function() {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(this.get("email"));
  }.property("email"),

  actions: {
    submit: function() {
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

      if (this.get("password") !== this.get("confirm_password")) {
        this.set("errors", "Passwords do not match");
        return;
      }

      this.set("canSubmit", false);

      var self = this;
      Ember.$.ajax({
        type: "POST",
        url: "/setup",
        contentType : 'application/json',
        data: JSON.stringify({ email: this.get("email"), password: this.get("password") })
      })
      .always(function() {
        self.set("canSubmit", true);
      })
      .fail(function(jqXHR) {
        var error = jqXHR.responseText ? jqXHR.responseText : jqXHR.statusText;
        self.set("errors", error);
      })
      .done(function() {
        self.transitionToRoute("");
      });
    }
  }
});
