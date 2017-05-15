import DS from "ember-data";

export default DS.Model.extend({
  email: DS.attr(),
  user_roles: DS.attr(),

  display_name: DS.attr(),
  full_name: DS.attr(),

  last_activity: DS.attr(),

  capabilities: DS.attr()
});
