import DS from "ember-data";

export default DS.Model.extend({

  capabilities: DS.attr(),
  display_name: DS.attr(),
  email: DS.attr(),
  full_name: DS.attr(),
  last_activity: DS.attr(),
  type: DS.attr(),
  user_roles: DS.attr(),

});
