import Component from "@ember/component";

export default Component.extend({
  expanded: false,
  error: null,

  classNames: "mx-3 my-2",
  classNameBindings: ["expanded", "error.is_interruption:interruption"],

  actions: {
    toggle_expanded() {
      this.toggleProperty("expanded");
    },
  },
});
