import DS from "ember-data";

export default DS.Model.extend({
  message: DS.attr(),
  timestamp: DS.attr("number"),
  filename: DS.attr(),
  lineno: DS.attr("number"),
  num_warnings: DS.attr("number"),
});
