import Controller from "@ember/controller";

export default Controller.extend({
  actions: {
    save() {
      let self = this;
      self
        .get("model")
        .save()
        .then(function() {
          self.router.transitionTo("admin.replications.index");
        });
    },
    cancel() {
      this.get("model").rollbackAttributes();
      this.router.transitionTo("admin.replications.index");
    },
  },
});
