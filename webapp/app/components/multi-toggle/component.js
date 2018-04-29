import Component from '@ember/component';

export default Component.extend({
  saving: false,

  display: null,
  options: null,

  options_and_display: function() {
    let display = this.get("display");
    let options = this.get("options");

    if (!display) {
      display = options;
    }

    let returned = {};

    for (let i = 0; i < options.length; ++i) {
      returned[options[i]] = display[i];
    }
    return returned;
  }.property("options", "display"),

  actions: {
    choose: function(option) {
      this.sendAction("action", option);
    }
  }
});
