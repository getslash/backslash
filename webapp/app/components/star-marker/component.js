import Component from "@ember/component";

export default Component.extend({
  tagName: "span",
  starred_object: null,
  actions: {
    toggle: function() {
      let object = this.get("starred_object");
      return object.toggle_starred().then(function() {
        return object.reload();
      });
    },
  },
});
