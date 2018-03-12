import EmberObject from '@ember/object';
import { inject as service } from '@ember/service';
import Controller from '@ember/controller';

export default Controller.extend({

  runtime_config: service(),

  metadata_links: function() {
    let returned = [];
    let metadata = this.get('test_metadata');

    for (let link of this.get('runtime_config').get_cached('test_metadata_links')) {
      let value = metadata[link.key];
      if (value) {
        returned.push(EmberObject.create({
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
