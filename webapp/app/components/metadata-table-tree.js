import Ember from 'ember';

export default Ember.Component.extend({
  treeCompliantMetadata: function() {
    var metadata = this.get('metadata');
    var compliantObject = [];
    this.createSubtree(compliantObject, '', metadata);
    return compliantObject;
  }.property('metadata'),

  /**
   This function creates a sbutree data structure to enable treegrid to present the metadata
   in a tree like table (sub objects in the json can be collapsed and expanded).

   The function fills array_to_append (output param) of table_lines (see below table_line format) made
   from the subtree at hand (treeObject).

   Treegrid needs two things - the current ID in the format - treegrid-1-3-1, and who is the parnet of the line
   (in the format treegrid-parent-1-3)

   Algorithm:
   We iterate all the properties in treeObject.
   If it is a complex object - we recursively call `createSubtree` on each element
   If not - we construct a regular table_line, with the addition that a text URL should be marked as isLink

   table_line structure:
   {
    'key': key, {String}
    'value': value, {String}
    'index': current node index. {String} format: 1-2-1-5
    'index-class': The class constructed from the `index`. {String} treegrid-1-2-1-5
    'parent': current node index. can be '' if parent is root - {String}. format: 1-2-1
    'parent-class': The class constructed from the `parent`. {String} treegrid-parent-1-2-1
    'isLink': is it a URL and needs to be <a/> {Boolean}
   }

   @method createSubtree
   @param {Array} array_to_append {Output param} - array of table_line.
   @param {String} parentIndex - The current subtree's parent index (can be '' if parent is root)
   in the format of 1-2-1-5...
   @param {Object} treeObject - the sub-tree object to work on (JSON)
   */
  createSubtree: function myself(array_to_append, parentIndex, treeObject) {
    var treeIndex = 1;
    var URL_regex = new RegExp('^(?:[a-z]+:)?//', 'i');
    var table_line;
    var currentIndex;
    for (var key in treeObject) {
      if (treeObject.hasOwnProperty(key)) {
        var value = treeObject[key];

        //prepare currentIndex
        if (parentIndex === '') {
          currentIndex = treeIndex;
        }
        else {
          currentIndex = parentIndex + '-' + treeIndex;
        }

        if (typeof value === "object") {
          //in a complex object - we still need to add a line - "headline" with the key of the json
          // (value is the sub object itself)
          table_line = {
            'key': key, 'value': '', 'index': currentIndex,
            'parent': parentIndex, 'isLink': false
          };

          //semi foul have a CSS class on the controller,
          // but in ember constructing those classes in the handlebars is difficult
          table_line['index-class'] = 'treegrid-' + currentIndex;
          if (parentIndex !== '') {
            table_line['parent-class'] = 'treegrid-parent-' + parentIndex;
          }
          array_to_append.push(table_line);
          //make a recursive call for the subelement, with currentIndex as the parent
          myself(array_to_append, currentIndex, value);
        }
        else  //not a complex object - is a leaf - add a regular line
        {
          var isLink = false;
          if ((typeof value === "string") && (URL_regex.test(value)))
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
