# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :server do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://bit.ly/dockerprecise64"
    config.vm.host_name = "server"
    config.vm.forward_port 80, 8080
    config.vm.provision :shell, :inline => "sudo mkdir ~root/.ssh"
    config.vm.provision :shell, :inline => "sudo cp ~vagrant/.ssh/authorized_keys ~root/.ssh/authorized_keys"
  end
end
