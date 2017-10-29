import Ember from 'ember';

export default Ember.Controller.extend({

  runtime_config: Ember.inject.service(),

  metadata_links: function() {
    let returned = [];
    let metadata = this.get('test_metadata');

    for (let link of this.get('runtime_config').get_cached('test_metadata_links')) {
      let value = metadata[link.key];
      if (value) {
        returned.push(Ember.Object.create({
          name: link.name,
          url: value,
          icon: link.icon,
        }));

      }
      return returned

    }
  }.property('test_metadata'),

  metadata_display_items: function() {
    return this.get('runtime_config').get_cached('test_metadata_display_items');
  }.property(),
});
