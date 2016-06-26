import DS from 'ember-data';

export default DS.Model.extend({
  message: DS.attr('string'),
  exception_type: DS.attr('string'),

  full_message: function() {
      let exc_type = this.get('exception_type');

      if (exc_type) {
          return exc_type + ': ' + this.get('message');
      }
      return this.get('message');
  }.property('exception_type', 'message'),

  timestamp: DS.attr(),
  traceback: DS.attr(),
  traceback_url: DS.attr(),
  type: DS.attr('string')
});
