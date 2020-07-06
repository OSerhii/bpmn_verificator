import os
from git import Repo
import lxml.etree


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def retrieve_source_from_repository(repo_name, branch):
    clone = "git clone https://SergeVL@bitbucket.org/ustudio-llc/{}.git".format(repo_name)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), repo_name)

    if not os.path.exists(path):
        os.system(clone)

    git = Repo(path).git

    with cd(repo_name):
        git.checkout(branch)
        git.pull("origin", branch)


def retrieve_delegates_from_source(path):
    dct = dict()
    lst = list()
    for path, dirs, files in os.walk(path):
        # if len(dirs) == 0:
        dct[os.path.basename(path)] = files
        delegates = [item.split(".")[0] for item in files]
        lst.extend(delegates)
    return lst


def retrieve_bpmn_file_names(path):
    lst = list()
    for path, dirs, files in os.walk(path):
        if '.git' in dirs:
            dirs.remove('.git')  # don't visit .git directories
        for file_name in files:
            if ".bpmn" in file_name:
                lst.append(file_name)
    return lst


def retrieve_delegates_from_bpmn(path):
    NSMAP = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL', 'camunda': 'http://camunda.org/schema/1.0/bpmn'}
    root = lxml.etree.parse(path).getroot()
    delegates = list()
    delegate_nodes = root.xpath('//bpmn:serviceTask[@camunda:delegateExpression]', namespaces=NSMAP)
    for node in delegate_nodes:
        delegate = node.attrib.get('{{{}}}delegateExpression'.format(NSMAP['camunda']))[2:-1]
        delegates.append(delegate)
    return delegates