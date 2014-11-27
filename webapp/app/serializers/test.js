import DS from 'ember-data';

export default DS.ActiveModelSerializer.extend({
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
