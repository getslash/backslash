import DS from 'ember-data';

export default DS.Model.extend({
  integerId: function() {
    return +this.get('id');
  }.property('id'),

  logicalId: DS.attr('string'),
  startTime: DS.attr('date'),
  endTime: DS.attr('date'),
  status: DS.attr('string'),
  hostname: DS.attr('string'),
  editedStatus: DS.attr('string'),
  productName: DS.attr('string'),
  productRevision: DS.attr('string'),
  productVersion: DS.attr('string'),
  userName: DS.attr('string'),
  tests: DS.hasMany('test', {async: true}, {inverse: 'session'}),
  sessionErrors: DS.attr(),
  sessionMetadata: DS.attr(),
  apiPath: DS.attr('string'),
  type: DS.attr('string'),


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

  isEditedStatus: function() {
    if(this.get('editedStatus'))
    {
      return true;
    }
    return false;
  }.property('editedStatus'),

  hasSessionErrors: function() {
    return (this.get('sessionErrors.length') > 0);
  }.property('sessionErrors')
});
