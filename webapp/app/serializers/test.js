import DS from 'ember-data';

export default DS.ActiveModelSerializer.extend({
  extractMeta: function(store, type, payload) {
    console.log(store, type, payload);
    if (payload && payload.metadata) {
      store.metaForType(type, payload.metadata);
      delete payload.metadata;
    }
  },

  normalizePayload: function(payload) {
    payload.tests = payload.result;
    delete payload.error;
    delete payload.result;
    delete payload.metadata;
    return payload;
  },

  keyForRelationship: function(rel, kind) {
    var underscored;
    if (kind === 'belongsTo') {
      underscored = rel.underscore();
      return underscored + "_id";
    } else {
      var singular = rel.singularize();
      underscored = singular.underscore();
      return underscored + "_ids";
    }
  }
});
