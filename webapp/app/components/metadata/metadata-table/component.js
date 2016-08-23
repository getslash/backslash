import Ember from 'ember';

export default Ember.Component.extend({

    additional: {},
    metadata: {},

    all_metadata: function() {
        let returned = {};

        [this.get('additional'), this.get('metadata')].forEach(function(obj) {
            for (var attrname in obj) {
                returned[attrname] = obj[attrname];
            }
        });
        return returned;
    }.property('additional', 'metadata'),

    slash_commandline: function() {
	let returned = this.get('metadata.slash.commandline');

	if (returned === undefined) {
	    returned = this.get('metadata')['slash::commandline'];
	}
	return returned;
    }.property('metadata'),

    slash_version: function() {
	let metadata = this.get('metadata') || {};
	let returned = metadata['slash::version'];
	if (!returned && metadata.slash !== undefined) {
	    returned = metadata.slash.version;
	}
	return returned;
    }.property('metadata'),


    slash_tags: function() {
	let metadata = this.get('metadata');

	let returned = metadata['slash::tags'];
	return returned;
    }.property('metadata'),

    slash_tags_without_values: function() {
	let tags = this.get('slash_tags');
	let returned = [];

	for (let tag of tags.names) {
	    if (!tags.values.hasOwnProperty(tag)) {
		returned.push(tag);
	    }
	}
	return returned;
    }.property('slash_tags'),

});
