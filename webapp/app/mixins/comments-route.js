import { hash } from 'rsvp';
import Mixin from '@ember/object/mixin';

export default Mixin.create({
  model() {
    let parent = this.get_parent();

    let query_params = { page_size: 200 };
    query_params[parent.constructor.modelName + "_id"] = parent.get("id");
    return hash({
      parent: parent,
      comments: this.store.query("comment", query_params)
    });
  },

  setupController(controller, model) {
    controller.setProperties(model);
  }
});
