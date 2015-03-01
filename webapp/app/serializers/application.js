import DS from 'ember-data';

export default DS.RESTSerializer.extend({

    extractMeta: function(store, type, payload) {
        if (payload && payload.metadata) {
            store.setMetadataFor(type, payload.metadata);
            delete payload.metadata;

        }
    },

    extractArray: function(store, type, payload) {
        var new_payload = {};
        var typename = type.toString().split(':')[1].split(':')[0];
        console.log('typename:' + typename);
        new_payload[typename + 's'] = payload.result;
        return this._super(store, type, new_payload);
    }
});
