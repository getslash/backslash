import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default Controller.extend({
  api: service(),
  router: service(),

  actions: {
    editReplication(replication) {
      this.get("router").transitionTo("admin.replications.edit", replication);
    },
    startReplication(replication) {
      this.get("api").call("start_replication", {
        id: parseInt(replication.id),
      });
      replication.set("active", true);
      replication.set("last_error", null);
    },

    pauseReplication(replication) {
      this.get("api").call("pause_replication", {
        id: parseInt(replication.id),
      });
      replication.set("active", false);
    },

    resetReplication(replication) {
      this.get("api").call("reset_replication", {
        id: parseInt(replication.id),
      });
      replication.set("active", false);
    },

    deleteReplication(replication) {
      if (
        window.confirm(
          `Are you sure you want to delete the replication to ${replication.get(
            "url"
          )}?`
        )
      ) {
        replication.destroyRecord();
      }
    },
  },
});
