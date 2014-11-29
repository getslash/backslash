import DS from 'ember-data';

export default DS.ActiveModelSerializer.extend({
    normalizePayload: function(payload) {
      payload.sessions = payload.result;
      delete payload.error;
      delete payload.result;
      delete payload.metadata;
      return payload;
    }

});
