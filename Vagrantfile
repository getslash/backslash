# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :server do |config|
    config.vm.box = "trusty64"
    config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    config.vm.host_name = "server"
    config.vm.forward_port 80, 8000
    config.vm.provision "ansible" do |ansible|
      ansible.groups = {
        "webapp" => ["server"],
        "db" => ["server"],
      }
      ansible.playbook = "ansible/site.yml"
      ansible.extra_vars = {
        install_with_debug: true
      }
      ansible.sudo = true
    end
  end
end
