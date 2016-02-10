import Ember from 'ember';
import config from '../../../config/environment';

export default Ember.Component.extend({

    email: null,
    tagName: 'img',

    attributeBindings: ['src'],
    classNames: ['img-circle'],
    classBindings: ['is_fake:fake-user'],

    is_fake: function() {
        if (this.get('real_email')) {
            return true;
        }
        return false;
    },

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
            console.log('setting fallback img', fallback);
            this.set('src', fallback);
        }.bind(this));
    },

    willDestroyElement: function(){
        this.$().off();
    }

});
