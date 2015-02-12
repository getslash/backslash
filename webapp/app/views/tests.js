import Ember from 'ember';

export default Ember.View.extend({
  metadata_queries: [Ember.Object.create({name: '', type: 'Exists', disableValue: true, queryValue:''})],
  metaTypes: ['Exists','Is Equal'],
  typeChanged: function(){
    //we can't register on observer on each array item, but iterating it is not too bad - there are few metaqueries
    this.get('metadata_queries').forEach(function(item) {
      Ember.set(item, "disableValue", item.type === "Exists");
    });
  }.observes('metadata_queries.@each.type'),

  actions: {
    addMetadataField: function () {
      this.get('metadata_queries').pushObject(Ember.Object.create({
        name: '',
        type: 'Exists',
        disableValue: true,
        queryValue: ''
      }));
    },
    removeMetadataField: function (context) {
      this.get('metadata_queries').removeObject(context);
    },

    search: function() {
      this.get('controller').set('metadataQueries', this.metadata_queries);
      this.get("controller").send("queryTests");
    }
  }
});
