import Ember from 'ember';
import { task, timeout } from 'ember-concurrency';

export default Ember.Mixin.create({

    INTERVAL_SECONDS: 30,


    refresh_loop: task(function * () {
        let self = this;
        while (true) {
            yield timeout(self.get('INTERVAL_SECONDS') * 1000);
            self.refresh();
        }
    }).on('init'),
});
