import Ember from 'ember';

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

export default Ember.Component.extend({
  showOneLine: true,

  formattedCode: function() {
    var code_string = this.get('traceback.code_string');

    //We are getting the code_string up to the exception line + empty one - we count on it here... (if it changes - this will fail)
    var splitted = code_string.split('\n');
    var last_code_lineno = this.get('traceback.lineno');
    var first_code_lineno = last_code_lineno - splitted.length + 1 + 1 /* extra +1 - last line is blank*/;
    var padding_size = last_code_lineno.toString().length + 1;

    splitted.forEach(function(element, index, theArray) {
      var str_code_lineno = (first_code_lineno + index).toString();

      theArray[index] = pad(str_code_lineno, padding_size, ' ') + " " + element;
    });

    splitted[splitted.length - 2] = '<span>' + splitted[splitted.length - 2] + "</span>";
    return splitted.slice(0,-1).join('\n'); //pop - last element is an empty line
  }.property('traceback.code_string'),

  actions: {
    toggleOneLine: function () {
      this.toggleProperty('showOneLine');
    }
  }

});
