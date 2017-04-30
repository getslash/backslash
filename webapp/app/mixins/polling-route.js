import Ember from 'ember';
import { task, timeout } from 'ember-concurrency';

export default Ember.Mixin.create({

    INTERVAL_SECONDS: 30,


    refresh_loop: task(function * () {
        let self = this;

        let callback = function() {
	    self.refresh();
        }
        
        while (true) {
            yield timeout(self.get('INTERVAL_SECONDS') * 1000);
	    let pred = self.should_auto_refresh;

	    if (pred !== undefined && pred.bind(self)()) {
                Ember.run.once(callback);
	    }
        }
    }).on('init'),

    actions: {
        error: function () {
            return false;
        }
  }

});
