import Ember from 'ember';

export default Ember.Service.extend({
    api: Ember.inject.service(),

    init() {
	this.set('_cache', Ember.Object.create());
    },

    get_all() {
	let self = this;
	return this.get('api').call('get_app_config').then(function(r) {
	    for (let attr in r.result) {
		if (r.result.hasOwnProperty(attr)) {
		    self.set(`_cache.${attr}`, r.result[attr]);
		}
	    }
	    return r.result;
	});
    },

    get_cached(name) {

        return this.get(`_cache.${name}`);
    },


});
