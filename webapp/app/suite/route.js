import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

    titleToken(model) {
	return `${model.get('name')}`;
    },

    model(params) {
	return this.store.find('suite', params.id);
    }
});
