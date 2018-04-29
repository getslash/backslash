import EmberObject from '@ember/object';
import Controller from '@ember/controller';

import RelativeItemJump from "../../../mixins/relative-item-jump";

export default Controller.extend(RelativeItemJump, {
  additional_metadata: function() {
    return {};
  }.property("test_model"),

  scm_details: function() {
    let self = this;
    let test_model = self.get("test_model");

    if (!test_model.get("scm")) {
      return {};
    }

    let returned = EmberObject.create({
      Revision: test_model.get("scm_revision"),
      "File Hash": test_model.get("file_hash"),
      "Local Branch": test_model.get("scm_local_branch"),
      "Remote Branch": test_model.get("scm_remote_branch"),
    });
    return returned;
  }.property("test_model"),

  params: function() {
    let params = this.get("test_model.parameters");
    if (params) {
      return params;
    }
    return this.get("test_model.variation");
  }.property("test_model")
});
