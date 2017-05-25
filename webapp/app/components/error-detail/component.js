import Ember from "ember";

export default Ember.Component.extend({
  error: null,
  all_expanded: false,

  init() {
    let self = this;
    self._super(...arguments);

    let url = self.get("error.traceback_url");
    if (url) {
      self.set("loading", true);
      Ember.$
        .ajax(url, { dataType: "json" })
        .then(function(data) {
          self.set("error.traceback", data.map(function(f) {return Ember.Object.create(f);}));
        })
        .always(function() {
          self.set("loading", false);
        });
    }
  },

  actions: {
    toggle_all_frames() {
      this.toggleProperty('all_expanded');
      let new_expanded = this.get('all_expanded');
      this.get('error.traceback').map(function(frame) {
        frame.set('expanded', new_expanded);
      });
    },
  },
});
