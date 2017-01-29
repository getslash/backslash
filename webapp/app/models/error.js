import DS from 'ember-data';

const _MAX_NUM_ERROR_LINES = 30;
const _MAX_NUM_ERROR_CHARS = 600;


export default DS.Model.extend({
  message: DS.attr('string'),
  exception_type: DS.attr('string'),

  full_message: function() {
      let exc_type = this.get('exception_type');

      if (exc_type) {
          return exc_type + ': ' + this.get('message');
      }
      return this.get('message');
  }.property('exception_type', 'message'),

  abbreviated_message: function() {
      let returned = this.get('full_message');
      let lines = returned.split(/\n/);
      let truncated = false;
      while (lines.length > _MAX_NUM_ERROR_LINES) {
          lines.pop();
          truncated = true;
      }

      returned = lines.join('\n');

      if (returned.length > _MAX_NUM_ERROR_CHARS) {
          returned = returned.substr(0, _MAX_NUM_ERROR_CHARS);
          truncated = true;

      }

      if (truncated) {
          returned += '...';
      }
      return returned;
  }.property('full_message'),

  timestamp: DS.attr(),
  traceback: DS.attr(),
  traceback_url: DS.attr(),
  type: DS.attr('string')
});
