import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import icePick

db = icePick.get_database('icePick_example', 'localhost')


class GithubRepoParser(icePick.Parser):
    def serialize(self):
        result = {
            "files": [],
        }

        for v in self.bs.find_all(class_="js-directory-link"):
            result['files'] += [v.text]
        return result


class GithubRepoRecorder(icePick.Recorder):
    struct = icePick.Structure(files=list())

    class Meta:
        database = db


class GithubRepoOrder(icePick.Order):
    recorder = GithubRepoRecorder
    parser = GithubRepoParser


def main():
    document = {
        "url": "https://github.com/teitei-tk/ice-pick/tree/master",
        "ua": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    }

    print('---download start---')
    order = GithubRepoOrder(document.get('url'), document.get('ua'))
    picker = icePick.Picker([order])
    picker.run()
    print("---finish---")

if __name__ == "__main__":
    main()
