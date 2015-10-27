# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :debian do |config|
    config.vm.box = "debian/jessie64"
    config.vm.host_name = "debian"
    config.vm.forward_port 80, 8000
  end

  config.vm.define :centos do |config|
    config.vm.box = "bento/centos-7.1"
    config.vm.host_name = "centos"
    config.vm.forward_port 80, 8001
  end

  config.vm.define :ubuntu do |config|
    config.vm.box = "bento/ubuntu-15.04"
    config.vm.host_name = "ubuntu"
    config.vm.forward_port 80, 8002
  end

  config.vm.define :arch do |config|
    config.vm.box = "terrywang/archlinux"
    config.vm.host_name = "arch"
    config.vm.forward_port 80, 8003
  end

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
      "webapp" => ["debian", "centos", "ubuntu", "arch"],
    }
    ansible.playbook = "ansible/site.yml"
    ansible.extra_vars = {
      "install_with_debug" => true,
      "ansible_python_interpreter" => "/usr/bin/python2"
    }
    ansible.sudo = true
  end
end
