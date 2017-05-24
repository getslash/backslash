import Ember from "ember";

export default Ember.Component.extend({
  classNames: "copyable-text",
  classNameBindings: ['preformatted'],

  value: null,
  copy_value: null,
  preformatted: false,
});
