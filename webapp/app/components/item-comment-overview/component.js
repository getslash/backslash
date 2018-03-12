import { inject as service } from '@ember/service';
import Component from '@ember/component';

export default Component.extend({
  display: service(),

  classNames: ["right-label", "fainter", "comments", "expand-on-hover"],

  classNameBindings: ["visible", "display.comments_expanded:expanded"],

  visible: function() {
    if (this.get("item.num_comments")) {
      return true;
    }
    return false;
  }.property("item")
});
