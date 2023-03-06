import time
import json
import yaml
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def on_modified(event):
    try:
        with open(event.src_path, encoding="utf-8") as yaml_file:
            yexp = yaml.safe_load(yaml_file)
            with open(event.src_path[:-4]+"json", 'w', encoding="utf-8") as json_file:
                json_file.write(json.dumps(yexp))

        print(f"File {event.src_path} has been modified. Converting to json...")

    except:
        print(f"There is some error in {event.src_path}. Cannot convert.")
    time.sleep(3)


if __name__ == "__main__":
    patterns = ["*.yaml"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_modified = on_modified

    path = input("Enter the path to watch: ")

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        print("Start watching...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
        print("Finish watching...")
