import Ember from 'ember';

export default Ember.Component.extend({

    display: Ember.inject.service(),

    classNames: ['right-label', 'fainter', 'comments', 'expand-on-hover'],

    classNameBindings: ['visible', 'display.comments_expanded:expanded'],

    visible: function() {
	if (this.get('item.num_comments')) {
	    return true;
	}
	return false;
    }.property('item'),
});
