import DS from 'ember-data';

export default DS.Model.extend({
  exception: DS.attr('string'),
  exception_type: DS.attr('string'),
  timestamp: DS.attr('date'),
  traceback: DS.attr(),
  type: DS.attr('string')
});
