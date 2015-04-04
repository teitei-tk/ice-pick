import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import icePick


def main():
    document = {
        "url": "https://www.google.co.jp/",
        "ua": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    }

    order = icePick.Order(document.get('url'), document.get('ua'))
    picker = icePick.Picker([order])
    picker.run()

if __name__ == "__main__":
    main()
