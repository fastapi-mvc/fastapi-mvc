# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "debian/bullseye64"
  config.vm.box_version = "11.20220328.1"
  config.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = "2"

      # https://github.com/hashicorp/vagrant/issues/11777#issuecomment-661076612
      vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
      vb.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]

      # NOTE: use host resolver to increase dl speeds for python
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end
  config.vm.provision "shell", inline: <<-SHELL
      echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20220328 bullseye main" > /etc/apt/sources.list
      echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian-security/20220328 bullseye-security main" >> /etc/apt/sources.list
      echo "deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20220328 bullseye-updates main" >> /etc/apt/sources.list
      apt-get update
      apt-get install --no-install-recommends -y curl make docker.io git golang python3 python3-pip python3-venv
      systemctl enable docker
      # NOTE: Fix resolving DNS in docker
      echo '{ "dns": ["192.168.0.1", "8.8.8.8"] }' > /etc/docker/daemon.json
      systemctl restart docker
      usermod -aG docker vagrant
      # Install kubectl
      curl -Lso /tmp/kubectl "https://storage.googleapis.com/kubernetes-release/release/v1.20.8/bin/linux/amd64/kubectl"
      install -m 755 /tmp/kubectl /usr/local/bin
      # Install minikube
      curl -Lso /tmp/minikube https://storage.googleapis.com/minikube/releases/v1.22.0/minikube-linux-amd64
      install -m 755 /tmp/minikube /usr/local/bin/

      # NOTE: no need to statrt minikube just yet
      #sudo -u vagrant MINIKUBE_IN_STYLE=0 minikube start --driver=docker 2> /dev/null
      # Install Helm
      curl -s https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

  SHELL
  # https://github.com/hashicorp/vagrant/issues/10002#issuecomment-419503397
  config.trigger.after :up do |t|
      t.info = "rsync auto"
      #t.run = {inline: "vagrant rsync-auto"}
      # If you want it running in the background switch these
      t.run = {inline: "bash -c 'vagrant rsync-auto &'"}
  end
  config.vm.synced_folder ".", "/syncd", type: "rsync"
  config.vm.boot_timeout = 600
end