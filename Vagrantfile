# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :server do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
    config.vm.host_name = "server"
    config.vm.forward_port 80, 8080
    config.vm.provision :shell, :inline => "test -d ~root/.ssh || sudo mkdir ~root/.ssh"
    config.vm.provision :shell, :inline => "sudo cp ~vagrant/.ssh/authorized_keys ~root/.ssh/authorized_keys"
  end
end
