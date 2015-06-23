import Ember from 'ember';

export default Ember.Mixin.create({

    actions: {
        refreshRoute: function() {
            console.log('refreshing');
            this.refresh();
        }
    }
});
