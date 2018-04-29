import ApplicationAdapter from './application';
import {Promise} from 'rsvp';
import {inject as service} from '@ember/service';

export default ApplicationAdapter.extend({

    api: service(),

    async deleteRecord(store, type, snapshot) {
        let result = await this.get('api').call('delete_replication', {id: parseInt(snapshot.id)});
    },

    async createRecord(store, type, snapshot) {
        let data = this.serialize(snapshot);
        let result = await this.get('api').call('create_replication', data);
        result.replication = result.result;
        delete result.result;
        return result;
    },
});
