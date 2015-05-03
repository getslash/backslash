import DS from 'ember-data';

export default DS.Model.extend({
  integerId: function() {
    return +this.get('id');
  }.property('id'),

  exception: DS.attr('string'),
  exceptionType: DS.attr('string'),
  timestamp: DS.attr('date'),
  traceback: DS.attr(),
  apiPath: DS.attr('string'),
  type: DS.attr('string')
});
