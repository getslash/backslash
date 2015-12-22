import DS from 'ember-data';

export default DS.Model.extend({
    name: DS.attr(),
    file_name: DS.attr(),
    class_name: DS.attr(),
});
