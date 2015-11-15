import DS from 'ember-data';

export default DS.Model.extend({
  message: DS.attr('string'),
  exception_type: DS.attr('string'),

  full_message: function() {
      return this.get('exception_type') + ': ' + this.get('message');
  }.property('exception_type', 'message'),

  timestamp: DS.attr('date'),
  traceback: DS.attr(),
  type: DS.attr('string')
});
