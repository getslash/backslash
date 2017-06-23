import DS from 'ember-data';

export default DS.Transform.extend({
  deserialize(serialized) {
    console.log('hey', serialized);
    return serialized;
  },

  serialize(deserialized) {
    return deserialized;
  }
});
