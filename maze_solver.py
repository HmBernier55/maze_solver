from tkinter import Tk, BOTH, Canvas
import time, random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed. . .")

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            p1 = Point(x1, y1)
            p2 = Point(x1, y2)
            self._win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x1, y1)
            p2 = Point(x1, y2)
            self._win.draw_line(Line(p1, p2), "white")
        if self.has_right_wall:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            self._win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x2, y1)
            p2 = Point(x2, y2)
            self._win.draw_line(Line(p1, p2), "white")
        if self.has_top_wall:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            self._win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x1, y1)
            p2 = Point(x2, y1)
            self._win.draw_line(Line(p1, p2), "white")
        if self.has_bottom_wall:
            p1 = Point(x1, y2)
            p2 = Point(x2, y2)
            self._win.draw_line(Line(p1, p2))
        else:
            p1 = Point(x1, y2)
            p2 = Point(x2, y2)
            self._win.draw_line(Line(p1, p2), "white")

    def draw_move(self, to_cell, undo=False):
        p1 = Point(((self._x1 + self._x2) / 2), ((self._y1 + self._y2) / 2))
        p2 = Point(((to_cell._x1 + to_cell._x2) / 2), ((to_cell._y1 + to_cell._y2) / 2))
        if undo:
            self._win.draw_line(Line(p1, p2), "gray")
        else:
            self._win.draw_line(Line(p1, p2), "red")


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col = []
            for j in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        cell_x1 = self._x1 + (self._cell_size_x * i)
        cell_y1 = self._y1 + (self._cell_size_y * j)
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y2 = cell_y1 + self._cell_size_y
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        c1 = self._cells[0][0]
        c1.has_top_wall = False
        self._draw_cell(0, 0)

        c2 = self._cells[self._num_cols - 1][self._num_rows - 1]
        c2.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            possible_direction_indexes = 0

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
                possible_direction_indexes += 1
            # right
            if i < (self._num_cols - 1) and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
                possible_direction_indexes += 1
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
                possible_direction_indexes += 1
            # down
            if j < (self._num_rows - 1) and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                possible_direction_indexes += 1

            # no possible directions
            if possible_direction_indexes == 0:
                self._draw_cell(i, j)
                return

            next_direction = random.randrange(possible_direction_indexes)
            next_cell_index = next_index_list[next_direction]

            # break down wall moving left
            if j == next_cell_index[1] and i > next_cell_index[0]:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # break down wall moving right
            if j == next_cell_index[1] and i < next_cell_index[0]:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # break down wall moving up
            if j > next_cell_index[1] and i == next_cell_index[0]:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # break down wall moving down
            if j < next_cell_index[1] and i == next_cell_index[0]:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            self._break_walls_r(next_cell_index[0], next_cell_index[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i, j):
        self._animate()

        # visit the current cell
        self._cells[i][j].visited = True

        # if we are at the end cell, we solved it!
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # moving left
        if (
            i > 0 
            and not self._cells[i][j].has_left_wall 
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # moving right
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # moving up
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # moving down
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False

    def solve(self):
        return self._solve_r(0, 0)





def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    print("maze created")
    is_solveable = maze.solve()
    if not is_solveable:
        print("maze can not be solved!")
    else:
        print("maze solved!")

    win.wait_for_close()

if __name__ == "__main__":
    main()