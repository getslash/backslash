import DS from "ember-data";

export default DS.Model.extend({
  integerId: function() {
    return +this.get("id");
  }.property("id"),

  exception: DS.attr("string"),
  exceptionType: DS.attr("date"),
  timestamp: DS.attr("date"),
  traceback: DS.attr(),
  test: DS.belongsTo("test", { async: true }, { inverse: "testErrors" }),
  apiPath: DS.attr("string"),
  type: DS.attr("string")
});
