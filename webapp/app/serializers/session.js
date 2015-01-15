import DS from 'ember-data';

export default DS.ActiveModelSerializer.extend({
  extractMeta: function(store, type, payload) {
    if (payload && payload.metadata) {
      store.metaForType(type, payload.metadata);
      delete payload.metadata;
    }
  },
    normalizePayload: function(payload) {
      payload.sessions = payload.result;
      delete payload.error;
      delete payload.result;
      return payload;
    }

});
