import Ember from "ember";

export default Ember.Mixin.create({
  api: Ember.inject.service(),

  new_comment: null,

  actions: {
    refresh() {
      this.send("refreshRoute");
      this.get("parent").reload();
    },
    post_comment() {
      let self = this;
      let parent = self.get("parent");
      let query_params = { comment: self.get("new_comment") };
      query_params[parent.constructor.modelName + "_id"] = parseInt(parent.id);
      self.get("api").call("post_comment", query_params).then(function() {
        self.set("new_comment", "");
        self.actions.refresh.bind(self)();
      });
    }
  }
});
