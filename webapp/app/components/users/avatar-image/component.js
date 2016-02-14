import Ember from 'ember';
import config from '../../../config/environment';

export default Ember.Component.extend({

    email: null,
    is_proxy: false,
    is_real: false,
    tagName: 'img',

    attributeBindings: ['src'],
    classNames: ['img-circle'],
    classNameBindings: ['is_proxy:proxy', 'is_real:real'],

    src: function() {
        let fallback_img = this.get('fallback_img_url');
        let returned = 'http://www.gravatar.com/avatar/' + window.md5(this.get('email'));
        if (fallback_img) {
            returned += '?d=404';
        } else {
            returned += '?d=mm';
        }
        return returned;
    }.property('email'),

    fallback_img_url: function() {
        let fallback = config.APP.avatars.fallback_image_url;
        if (!fallback) {
            return null;
        }
        return fallback.replace('__EMAIL__', this.get('email'));
    }.property(),

    didInsertElement: function() {
        let self = this;
        this.$().on('error', function() {
            let fallback = self.get('fallback_img_url');
            this.set('src', fallback);
        }.bind(this));
    },

    willDestroyElement: function(){
        this.$().off();
    }

});
