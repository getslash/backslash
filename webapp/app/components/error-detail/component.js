import Ember from "ember";

export default Ember.Component.extend({
  error: null,
  all_expanded: false,

  sorted_exception_attributes: function() {
    let returned = [];
    let attrs = this.get('error.exception_attributes');
    for (let var_name in attrs) {
      if (attrs.hasOwnProperty(var_name)) {
        returned.append
      }
    }
  }.property('error.exception_attributes'),

  init() {
    let self = this;
    self._super(...arguments);

    let url = self.get("error.traceback_url");
    if (url) {
      self.set("loading", true);
      Ember.$
        .ajax(url, { dataType: "json" })
        .then(function(data) {
          let traceback = data;
          let exception_attributes = null;
          if (traceback.traceback !== undefined) {
            traceback = data.traceback;
            exception_attributes = self._parse_exception_attributes(data.exception.attributes);
          }
          self.set("error.traceback", traceback.map(function(f) {return Ember.Object.create(f);}));
          self.set("error.exception_attributes", exception_attributes);
        })
        .always(function() {
          self.set("loading", false);
        });
    }
  },

  _parse_exception_attributes(attrs) {
    let returned = [];

    for (let var_name in attrs) {
      if (attrs.hasOwnProperty(var_name)) {
        returned.push({name: var_name, display_name: var_name, value: {value: attrs[var_name]}});
      }
    }
    return returned;
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
