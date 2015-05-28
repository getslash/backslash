import DS from 'ember-data';

export default DS.Model.extend({

  start_time: DS.attr('date'),
  end_time: DS.attr('date'),
  status: DS.attr('string'),


});
