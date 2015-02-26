import DS from 'ember-data';

export default DS.ActiveModelSerializer.extend({
  extractMeta: function(store, type, payload) {
    if (payload && payload.metadata) {
      store.setMetadataFor(type, {metadata: payload.metadata});
    }
    if ('metadata' in payload) // can be null, delete it anyway
    {
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
