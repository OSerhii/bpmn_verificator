import os
from service import retrieve_source_from_repository, retrieve_delegates_from_source, retrieve_bpmn_file_names, \
    retrieve_delegates_from_bpmn

JAVA_DELEGATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "orchestrator/src/main/java/com/procurement/orchestrator/delegate")
KOTLIN_DELEGATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "orchestrator/src/main/kotlin/com/procurement/orchestrator/infrastructure/bpms/delegate")
BPMN_DELEGATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "orchestrator/src/main/resources/processes")


retrieve_source_from_repository("orchestrator", "dev")

java_delegates = retrieve_delegates_from_source(JAVA_DELEGATES_PATH)
kotlin_delegates = retrieve_delegates_from_source(KOTLIN_DELEGATES_PATH)
source_delegates = java_delegates + kotlin_delegates


files = retrieve_bpmn_file_names(BPMN_DELEGATES_PATH)
error_lst = list()

for file in files:
    path = os.path.join(BPMN_DELEGATES_PATH, file)
    bpmn_delegates = retrieve_delegates_from_bpmn(path)

    for delegate in bpmn_delegates:
        normalized_delegate = delegate[0].upper() + delegate[1:]
        if normalized_delegate not in source_delegates:
            error_lst.append({file: normalized_delegate})

if len(error_lst) > 0:
    raise ValueError("Not all delegates implemented. Delegates list: {}".format(error_lst))
