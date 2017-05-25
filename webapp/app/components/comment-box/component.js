import Ember from "ember";

export default Ember.Component.extend({
  editing: false,

  actions: {
    delete_comment() {
      let self = this;
      if (
        !window.confirm("Are you sure you would like to delete this comment?")
      ) {
        return;
      }
      let c = this.get("comment");
      c.deleteRecord();
      c.save().then(function() {
        self.sendAction("comment_deleted");
      });
    },

    start_editing() {
      let self = this;
      self.set("editing", true);
      Ember.run.scheduleOnce("afterRender", self, function() {
        self.$("textarea").focus();
      });
    },

    cancel_editing() {
      this.set("editing", false);
      this.get("comment").rollbackAttributes();
    },

    save() {
      this.set("editing", false);
      this.get("comment").save();
    }
  }
});
