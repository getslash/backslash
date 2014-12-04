import DS from 'ember-data';

export default DS.Model.extend({
  logicalId: DS.attr('string'),
  startTime: DS.attr('date'),
  endTime: DS.attr('date'),
  status: DS.attr('string'),
  hostname: DS.attr('string'),
  productName: DS.attr('string'),
  productRevision: DS.attr('string'),
  productVersion: DS.attr('string'),
  userName: DS.attr('string'),
  tests: DS.hasMany('test', {async: true}, {inverse: 'session'}),

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

  hasErrors: function() {
    var status = this.get('status');
    return ((status === 'FAILURE') || (status === 'ERROR'));
  }.property('status'),

  isRunning: function() {
    return (this.get('status') === 'RUNNING');
  }.property('status')
});
