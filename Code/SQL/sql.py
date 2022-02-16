import csv
import os

cur_path = os.path.dirname(os.path.realpath(__file__))


class Table:

    delete_go_back = []

    def __init__(self, name, header=[]):
        self.name = name
        self.file_name = cur_path + '/' + self.name + ".csv"
        if not os.path.exists(self.file_name):
            if len(header) > 0:
                print("WARNING: File {}.csv not exist, create file with given header.".format(name))
                self.headers = header
                with open(self.file_name, 'w', newline='') as f:
                    f_csv = csv.DictWriter(f, self.headers)
                    f_csv.writeheader()
            else:
                raise FileExistsError("File {}.csv not exist and there's no legal input param [header] to create one.".format(name))
        else:
            with open(self.file_name, 'r', newline='') as f:
                f_csv = csv.reader(f)
                self.headers = list(f_csv)[0]

    # get header of this table
    def get_headers(self):
        return self.headers

    # get file name with ".csv"
    def get_filename(self):
        return self.file_name

    # get file name without ".csv"
    def get_name(self):
        return self.name

    # insert a certain row as same items number with table
    # item in row must has type [string]
    def insert(self, row: list):
        if not len(row) == len(self.headers):
            raise IndexError("Need row length: {} while given {}".format(len(self.headers), len(row)))

        # check existence
        with open(self.file_name, 'r', newline='') as f:
            f_read = csv.reader(f)
            for r in list(f_read)[1:]:
                if r[0] == row[0]:
                    if r == row:
                        # raise AssertionError("Row {} has already exist".format(row))
                        return
        with open(self.file_name, 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows([row])

    # insert several rows as same items number with table
    # item in a single row must has type [string]
    def multi_row_insert(self, rows):
        for row in rows:
            self.insert(row)

    # find a certain row with given tags {header1: item1, ...}, then show it with a given function
    def find(self, tags: dict, show=print):
        # check feasibility of tag & modified:
        for key in tags.keys():
            if key not in self.headers:
                raise KeyError("File {} has no header {}".format(self.name, key))

        tags_index = {}
        for key in tags.keys():
            tags_index[key] = self.headers.index(key)
        res = list()
        with open(self.file_name, 'r', newline='') as f:
            f_csv = csv.reader(f)
            for row in list(f_csv)[1:]:
                for key in tags:
                    if not row[tags_index[key]] == tags[key]:
                        break
                else:
                    res.append(row)
        #show(res)
        return res

    # find several rows with given tags {header1: item1, ...}
    # then modify each of them with modifier {header1: new item1, ...}
    def modify(self, tags: dict, modifier: dict):
        # check feasibility of tag & modified:
        for key in tags.keys():
            if key not in self.headers:
                raise KeyError("File {} has no header {}".format(self.name, key))
        for key in modifier.keys():
            if key not in self.headers:
                raise KeyError("File {} has no header {}".format(self.name, key))

        tags_index = {}
        for key in tags.keys():
            tags_index[key] = self.headers.index(key)
        res = []
        prepare = []
        with open(self.file_name, 'r', newline='') as f:
            f_csv = csv.reader(f)
            for row in list(f_csv)[1:]:
                for key in tags:
                    if not row[tags_index[key]] == tags[key]:
                        res.append(row)
                        break
                else:
                    prepare.append(row)

        modifier_index = {}
        for key in modifier.keys():
            modifier_index[key] = self.headers.index(key)
        for row in prepare:
            for key in modifier.keys():
                row[modifier_index[key]] = modifier[key]
        res.extend(prepare)
        res.insert(0, self.headers)

        with open(self.file_name, 'w', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(res)

    # delete several rows with given tags {header1: item1, ...}
    def delete(self, tags: dict):
        self.delete_go_back = []
        # check feasibility of tag & modified:
        for key in tags.keys():
            if key not in self.headers:
                raise KeyError("File {} has no header {}".format(self.name, key))

        tags_index = {}
        for key in tags.keys():
            tags_index[key] = self.headers.index(key)
        res = []
        with open(self.file_name, 'r', newline='') as f:
            f_csv = csv.reader(f)
            for row in list(f_csv)[1:]:
                for key in tags:
                    if not row[tags_index[key]] == tags[key]:
                        res.append(row)
                        break
                else:
                    self.delete_go_back.append(row)

        res.insert(0, self.headers)
        with open(self.file_name, 'w', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(res)

    # if you accidentally delete a/several row(s), call delete_recall() to re-add it to the table
    # NOTION: you only have one chance to recall after a delete() called
    def delete_recall(self):
        if len(self.delete_go_back) == 0:
            print("Nothing happened since there's nothing to recall")
            return
        with open(self.file_name, 'a+', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self.delete_go_back)

        self.delete_go_back = []

    # clear the whole table without header
    def clear_without_header(self):
        with open(self.file_name, 'w', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows([self.headers])

    # destroy this table which means both this instance and file it linked will be deleted
    def destroy(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            del self
        else:
            raise FileNotFoundError("Nothing to delete")
