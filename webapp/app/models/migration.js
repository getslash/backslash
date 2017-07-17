import DS from 'ember-data';

export default DS.Model.extend({

  name: DS.attr(),
  started_time: DS.attr("number"),
  finished_time: DS.attr("number"),
  total_num_objects: DS.attr("number"),
  remaining_num_objects: DS.attr("number"),
  started: DS.attr("boolean"),
  finished: DS.attr("boolean"),

  num_finished_objects: function() {
    let total = this.get('total_num_objects');
    let remaining = this.get('remaining_num_objects');

    if (!total) {
      return 0;
    }

    if (remaining === 0) {
      return total;
    }

    if (!remaining) {
      return 0;
    }

    return total - remaining;


  }.property('total_num_objects', 'remaining_num_objects'),

  percentage: function() {

    let total = this.get('total_num_objects');

    if (total === 0) {
      return 100;
    }

    return Math.trunc((this.get('num_finished_objects') / total) * 100);
  }.property('num_finished_objects', 'total_num_objects'),

});
