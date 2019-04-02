import DS from "ember-data";

export default DS.Model.extend({
  name: DS.attr(),
  last_activity: DS.attr(),
  type: DS.attr(),
});
