# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :server do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://dl.dropbox.com/u/1537815/precise64.box"
    config.vm.host_name = "server"
    config.vm.forward_port 80, 8080
    config.vm.provision :shell, :path => "scripts/_internal_vagrant_setup.sh"
  end
end
