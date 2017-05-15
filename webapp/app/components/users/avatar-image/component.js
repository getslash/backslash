import Ember from 'ember';

export default Ember.Component.extend({

    email: null,
    is_proxy: false,
    is_real: false,
    tagName: 'img',

    attributeBindings: ['src'],
    classNames: ['img-circle', 'avatar-image'],
    classNameBindings: ['is_proxy:proxy', 'is_real:real'],

    src: function() {
        let returned = 'https://www.gravatar.com/avatar/' + window.md5(this.get('email'));
        returned += '?d=mm';
        return returned;
    }.property('email'),
});
