export default function config() {
    this.passthrough('/runtoken/**');
    this.passthrough('/reauth');
    this.passthrough('/login');
    this.passthrough('/logout');
    this.passthrough('/rest/**');
    this.passthrough('/api/**');
}

export function testConfig() {

    this.post('/api/get_app_config', function() {
	return {};
    });

    this.post('/api/get_preferences', function() {
	return {
	    result: {
		time_format: 'default_time_format',
	    }
	};
    });

    this.post('/api/set_preference', function(db, request) {
	let value = JSON.parse(request.requestBody).value;
	return {
	    result: value
	};
    });

}
