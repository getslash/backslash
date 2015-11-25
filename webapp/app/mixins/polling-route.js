import Ember from 'ember';

export default Ember.Mixin.create({

  _poll_schedule: null,
  INTERVAL_SECONDS: 30,

  activate: function() {
    let self = this;
    self._super();
    self._set_next_refresh();
  },

  _set_next_refresh: function() {
    let self = this;
    self.set('_poll_schedule', Ember.run.later(self, function() {
      self.refresh();
      self._set_next_refresh();
    }, self.get('INTERVAL_SECONDS') * 1000));
  },

  deactivate: function() {
    this._super();
    this._clear_interval();
  },

  _clear_interval: function() {
    let self = this;
    Ember.run.cancel(self.get('_poll_schedule'));
    self.set('_poll_schedule', null);
  },
});
