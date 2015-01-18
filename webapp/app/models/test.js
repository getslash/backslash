import DS from 'ember-data';

export default DS.Model.extend({
  integerId: function() {
    return +this.get('id');
  }.property('id'),

  logicalId: DS.attr('string'),
  startTime: DS.attr('date'),
  endTime: DS.attr('date'),
  duration: DS.attr('number'),
  status: DS.attr('string'),
  name: DS.attr('string'),
  testMetadata: DS.attr(),
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
  }.property('endTime'),

  isError: function() {
    return (this.get('status') === 'ERROR');
  }.property('status'),

  isFailure: function() {
    return (this.get('status') === 'FAILURE');
  }.property('status'),

  isSuccess: function() {
    return (this.get('status') === 'SUCCESS');
  }.property('status'),

  isRunning: function() {
    return (this.get('status') === 'RUNNING');
  }.property('status'),

  isInterrupted: function() {
    return (this.get('status') === 'INTERRUPTED');
  }.property('status'),

  isSkipped: function() {
    return (this.get('status') === 'SKIPPED');
  }.property('status')

});
