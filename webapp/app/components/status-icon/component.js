import Component from '@ember/component';

export default Component.extend({
  status: null,
  session_model: null,

  status_lower: function() {
    let returned = this.get("status");
    if (returned) {
      returned = returned.toLowerCase();
    }
    return returned;
  }.property("status"),

  spaced: true,
  classNames: "status-icon",
  classNameBindings: ["spaced:spaced", "status_lower"],
  tagName: "span"
});
