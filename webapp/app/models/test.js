import DS from 'ember-data';

export default DS.Model.extend({
  logicalId: DS.attr('string'),
  startTime: DS.attr('date'),
  endTime: DS.attr('date'),
  duration: DS.attr('number'),
  status: DS.attr('string'),
  name: DS.attr('string'),
  testMetadata: DS.attr('string'),
  numErrors: DS.attr('number'),
  numFailures: DS.attr('number'),
  skipped: DS.attr('boolean'),
  session: DS.belongsTo('session', {async: true}, {inverse:'tests'}),

  //ember date needs the wrong units
  properStartTime: function() {
    var d = new Date(0);
    d.setUTCSeconds(this.get('startTime'));
    return d;
  }.property('startTime'),
  properEndTime: function() {
    if (this.get('endTime') == null)
    {
      return null;
    }
    var d = new Date(0);
    d.setUTCSeconds(this.get('endTime'));
    return d;
  }.property('endTime')
});
