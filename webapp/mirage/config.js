export default function config() {
    this.passthrough('/reauth');
    this.passthrough('/login');
    this.passthrough('/rest/**');
    this.passthrough('/api/**');
}

export function testConfig() {

    this.post('/api/get_app_config', function() {
	return {};
    });
}
