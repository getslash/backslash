import Ember from 'ember';
import InfinityRoute from 'ember-infinity/mixins/route';


export default Ember.Mixin.create(InfinityRoute, {

    perPageParam: "page_size",
    pageParam: "page",
    totalPagesParam: "meta.pages_total",


    model() {
	const model_name = this.get('model_name');

	return Ember.RSVP.hash({
	    suites: this.infinityModel(
		model_name, {
		    perPage: 50,
		    startingPage: 1,
		    modelPath: `controller.${model_name.pluralize()}`
		}),
	});
    },

    setupController(controller, model) {
	this._super(controller, model);
	controller.setProperties(model);
    },
});
