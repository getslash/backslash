import $ from 'jquery';
import { inject as service } from '@ember/service';
import BaseController from "../controllers/base";

export default BaseController.extend({
  session: service(),

  path_tracker: service(),

  _path_observer: function() {
    this.get("path_tracker").set("path", this.get("currentPath"));
  }.observes("currentPath"),

  actions: {
    loading(transition) {
      let self = this;
      self.set("loading", true);
      transition.promise.finally(function() {
        self.set("loading", false);
      });
    },

    logout: function() {
      let self = this;
      $
        .ajax({
          url: "/logout",
          type: "POST"
        })
        .then(function() {
          self.get("session").invalidate();
        });
    }
  }
});
