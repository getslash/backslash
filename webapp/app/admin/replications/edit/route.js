import Route from "@ember/routing/route";

export default Route.extend({
  model({ replication_id }) {
    return this.store.findRecord("replication", replication_id);
  },

  renderTemplate: function() {
    this.render("admin.replications.new", {
      controller: "admin.replications.edit",
    });
  },
});
