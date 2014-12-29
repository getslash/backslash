import Ember from 'ember';

export default Ember.Controller.extend({
  treeCompliantMetadata: function() {
    var model = this.get('model');

    var metadata = model.get('testMetadata');
    var compliantObject = [];
    this.createSubtree(compliantObject, '', metadata);
    return compliantObject;
  }.property('model.testMetadata'),

  createSubtree: function myself(array_to_append, parentIndex, treeObject) {
    var treeIndex = 1;
    var r = new RegExp('^(?:[a-z]+:)?//', 'i');
    var table_line;
    var currentIndex;
    for (var key in treeObject) {
      if (treeObject.hasOwnProperty(key)) {
        var value = treeObject[key];
        if (typeof value === "object") {
          if (parentIndex === '') {
            currentIndex = treeIndex;
          }
          else {
            currentIndex = parentIndex + '-' + treeIndex;
          }
          table_line = {
            'key': key, 'value': '', 'index': currentIndex,
            'parent': parentIndex, 'isLink': false
          };
          //semi foul to do it on a controller, but in ember it is difficult to do inside the handlebars
          // (causes tight coupling between controller and tree plugin choice)
          table_line['index-class'] = 'treegrid-' + currentIndex;
          if (parentIndex !== '') {
            table_line['parent-class'] = 'treegrid-parent-' + parentIndex;
          }
          array_to_append.push(table_line);
          myself(array_to_append, currentIndex, value);
        }
        else
        {
          if (parentIndex === '')
          {
            currentIndex = treeIndex;
          }
          else {
            currentIndex = parentIndex + '-' + treeIndex;
          }
          var isLink = false;
          if ((typeof value === "string") && (r.test(value)))
          {
            isLink = true;
          }
          table_line = {'key': key, 'value':treeObject[key],
            'index':currentIndex, 'parent':parentIndex, 'isLink':isLink};
          table_line['index-class'] = 'treegrid-' + currentIndex;
          if (parentIndex !== '') {
            table_line['parent-class'] = 'treegrid-parent-' + parentIndex;
          }
          array_to_append.push(table_line);
        }
        treeIndex++;
      }
    }
  }

});

