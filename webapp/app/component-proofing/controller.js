import $ from 'jquery';
import { later } from '@ember/runloop';
import Controller from '@ember/controller';

export default Controller.extend({
  /* Avatar */
  admin: true,
  moderator: false,
  large: true,

  search: null,

  queryParams: ["search"],

  toggle_visible: function() {
    let term = this.get("search");
    later(function() {
      $(".proofing-example h3").each(function() {
        let heading = $(this);
        if (!term || heading.text().indexOf(term) !== -1) {
          heading.parent().css("display", "block");
        } else {
          heading.parent().css("display", "none");
        }
      });
    });
  }
    .observes("search")
    .on("didInsertElement"),

  use_real_email: false,

  avatar_email: "vmalloc@gmail.com",

  real_email: function() {
    if (this.get("use_real_email")) {
      return "spatz@psybear.com";
    }
    return null;
  }.property("use_real_email"),

  actions: {
    set_test_status(status) {
      this.set("model.test_result.status", status);
    }
  }
});
