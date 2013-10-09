from .deployment_test import DeploymentTest

class SanityTest(DeploymentTest):
    def test__sanity(self):
        self.request("get", "/").raise_for_status()
