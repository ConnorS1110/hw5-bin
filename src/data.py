import math
import utility as util
from collections.abc import Iterable
from utility import *
import update

class DATA:

    def __init__(self):
        self.rows = []
        self.cols = None

    def read(self, sFile):
        """
        Function Name:
            read
        Inputs:
            self: an instance of a class
            sFile: a string representing the path to a CSV file to be read
        Outputs:
            data: a DATA object that contains the information read from the CSV file
        """
        data = DATA()
        callback = lambda t: update.row(data, t)
        util.readCSV(sFile, callback)
        return data

    def clone(self, data, ts = None):
        """
        Function:
            clone
        Description:
            Creates a clone of the DATA object and returns it
        Input:
            self - current DATA instance
            data - data to be cloned
        Output:
            data - Clone of DATA object
        """
        data1 = update.row(DATA(), data.cols.names)
        for t in (ts or []):
            update.row(data1, t)
        return data1

    def dist(self, row1, row2, cols = None):
        """
        Function:
            dist
        Description:
            Finds normalized distance between row1 and row2
        Input:
            self - current DATA instance
            row1 - First row
            row2 - Second row
            cols - cols to use as the data for distance
        Output:
            Normalized distance between row1 and row2
        """
        n, d = 0, 0
        for col in (cols or self.cols.x):
            n += 1
            d += col.dist(row1.cells[col.at], row2.cells[col.at]) ** util.args.p
        return (d / n) ** (1 / util.args.p)

    def around(self, row1, rows = None, cols = None):
        """
        Function:
            around
        Description:
            Sorts rows by distance to row1
        Input:
            self - current DATA instance
            row1 - Central row to do sorting by distance around
            rows - Rows to compare to distance from row1
            cols - cols to use as the data for sorting by distance to row1
        Output:
            Sorted list of rows by their distance to row1
        """
        if isinstance(rows, Iterable):
            iterable = rows
        else:
            iterable = self.rows

        rows_with_distance = [(row2, self.dist(row1, row2, cols)) for row2 in iterable]
        sorted_rows = sorted(rows_with_distance, key=lambda x: x[1])
        return [(row, dist) for row, dist in sorted_rows]

    def furthest(self, row1, rows, cols = None):
                t = self.around(row1, rows, cols)
                return t[-1][0]

    def cluster(self, rows = None, cols = None, above = None):
        """
        Function:
            cluster
        Description:
            Returns clustered rows by recursively splitting data
        Input:
            self - current DATA instance
            rows - rows to cluster
            cols - cols to cluster
            above - Previous point of split
        Output:
            Clustered rows
        """
        rows = rows if rows else self.rows
        # min = min if min else len(rows) ** util.args.min
        cols = cols if cols else self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) >= 2:
            left, right, node["A"], node["B"], node["mid"], node["C"] = self.half(rows, cols, above)
            node["left"] = self.cluster(left, cols, node["A"])
            node["right"] = self.cluster(right, cols, node["B"])
        return node

    def sway(self, rows = None, min = None, cols = None, above = None):
        """
        Function:
            sway
        Description:
            Finds the best half of the data by recursion
        Input:
            self - current DATA instance
            rows - rows to sway
            cols - cols to sway
            min - Determines when recursion stops
            above - Previous point of split
        Output:
            Swayed rows
        """
        rows = rows if rows else self.rows
        min = min if min else len(rows) ** util.args.min
        cols = cols if cols else self.cols.x
        node = {"data": self.clone(rows)}

        if len(rows) > 2 * min:
           left, right, node["A"], node["B"], node["mid"], _ = self.half(rows, cols, above)
           if self.better(node["B"], node["A"]):
               left, right, node["A"], node["B"] = right, left, node["B"], node["A"]
           node["left"] = self.sway(left,  min, cols, node["A"])

        return node
