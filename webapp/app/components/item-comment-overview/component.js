import Ember from 'ember';

export default Ember.Component.extend({

    classNames: ['right-label', 'fainter', 'comments', 'expand-on-hover'],

    classNameBindings: ['visible', 'expanded'],

    visible: function() {
	if (this.get('item.num_comments')) {
	    return true;
	}
	return false;
    }.property('item'),
});
