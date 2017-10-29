import DS from "ember-data";

export default DS.Model.extend({
  file_name: DS.attr(),
  class_name: DS.attr(),
  name: DS.attr(),
  type: DS.attr(),

  location: function() {
    let returned = this.get('file_name');
    let class_name = this.get('class_name');
    if (class_name) {
      returned += `::${class_name}`;
    }
    return returned;

  }.property('file_name', 'class_name'),
});
