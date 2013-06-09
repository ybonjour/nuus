from boto import ec2
import pickle
import time
import sys
import os
from string import Formatter

INSTANCES_FILE = "services_store"
USAGE = "USAGE: python deploy.py [start | stop] ([instance_file={0}])".format(INSTANCES_FILE)

class ServiceController(object):

    def __init__(self):
        self.reservations = {}
        self.conn = None
        self.install_scripts = {
            "indexing": "install_indexing.sh",
            "feeds": "install_feeds.sh",
            "articles": "install_articles.sh",
            "clustering": "install_clustering.sh",
            "collector": "install_feedcollector.sh"
        }
        self.servicenames = {
            "indexing": "nuus-indexing",
            "feeds": "nuus-feeds",
            "articles": "nuus-articles",
            "clustering": "nuus-clustering",
        }

    def get_connection(self):
        if not self.conn:
            self.conn = ec2.connect_to_region("eu-west-1")
        return self.conn

    def update_sources(self):
        for ip in self.get_ips().values():
            os.system("ssh -i nuus.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ubuntu@{ip} '(cd ~/nuus; git pull)'".format(ip=ip))

    def install_services(self):
        template = "ssh -i nuus.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ubuntu@{ip} '(cd ~/nuus; sudo ./{install_script})'"
        for name, ip in self.get_ips().iteritems():
            command = template.format(ip=ip, install_script=self.install_scripts[name])
            os.system(command)

    def start_services(self):
        template = "ssh -i nuus.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ubuntu@{ip} 'sudo service {servicename} start'"
        for name, ip in self.get_ips().iteritems():
            if not name in self.servicenames:
                continue
            command = template.format(ip=ip, servicename=self.servicenames[name])
            os.system(command)

    def copy_file(self, filename):
        template = "scp -i nuus.pem -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no {local_file} ubuntu@{ip}:{remote_file}"
        for name, ip in self.get_ips().iteritems():
            command = template.format(ip=ip, local_file=filename, remote_file=os.path.join("nuus", filename))
            os.system(command)

    def start_instances(self, collecting):
        conn = self.get_connection()
        self.reservations["indexing"] = conn.run_instances(image_id="ami-3e46514a", key_name="nuus")
        self.reservations["feeds"] = conn.run_instances(image_id="ami-3e46514a", key_name="nuus")
        self.reservations["articles"] = conn.run_instances(image_id="ami-3e46514a", key_name="nuus")
        self.reservations["clustering"] = conn.run_instances(image_id="ami-3e46514a", key_name="nuus")

        if collecting:
            self.reservations["collector"] = conn.run_instances(image_id="ami-3e46514a", key_name="nuus")

    def stop(self):
        conn = self.get_connection()
        for reservation in self.reservations.values():
            instance_id = reservation.instances[0].id
            conn.terminate_instances([instance_id])

    def produce_config(self, template_path, output_path):
        with open(template_path) as template:
            content = Formatter().vformat(template.read(), None, self.get_ips())
        with open(output_path, "w") as output:
            output.write(content)

    def get_ips(self):
        conn = self.get_connection()
        ips = {}
        for name, reservation in self.reservations.iteritems():
            ips[name] = [r for r in conn.get_all_instances() if r.id == reservation.id][0].instances[0].public_dns_name
        return ips

    def save_current_instances(self, filename):
        with open(filename, "w") as f:
            pickle.dump(self.reservations, f)

    def load_instances(self, filename):
        with open(filename) as f:
            self.reservations = pickle.load(f)

def start(filename):
    services = ServiceController()
    services.start_instances(True)
    services.save_current_instances(filename)
    print("Wait for services to start.")
    time.sleep(60)
    print(services.get_ips())
    print("Producing config file")
    services.produce_config("common/nuus_template.cfg", "common/nuus_prod.cfg")
    print("Updating sources")
    services.update_sources()
    print("Copying config file")
    services.copy_file("common/nuus_prod.cfg")
    print("Installing services")
    services.install_services()
    print("Start services")
    services.start_services()

def stop(filename):
    services = ServiceController()
    services.load_instances(filename)
    services.stop()

def run(command, filename=INSTANCES_FILE):
    if command == "start":
        start(filename)
    elif command == "stop":
        stop(filename)
    elif command == "restart":
        stop(filename)
        start(filename)
    else:
        print(USAGE)

if __name__ == "__main__":
    arguments = sys.argv[1:]
    if len(arguments) == 1:
        run(arguments[0])
    elif len(arguments) == 2:
        run(arguments[0], arguments[1])
    else:
        print(USAGE)
        exit()