


class SVGZygalskiSheetShort:

    SCALE = 0.5
    CELL_SIZE = 24
    CELL_BORDER_WIDTH = 2
    SHEET_BORDER_WIDTH = CELL_SIZE
    LETS_LEFT_OFFSET = -17
    LETS_RIGHT_OFFSET = (CELL_SIZE * 26) + 9
    LETS_TOP_OFFSET = -3.5 * 2
    LETS_BOTTOM_OFFSET = (CELL_SIZE * 26) + 16
    WHITE_BORDER_WIDTH = 1
    SHEET_ID_X = 20 * 2
    SHEET_ID_Y = 20 * 2
    LETS_SIZE = 7 * 2
    LETS_FONT = "sans-serif"
    SHEET_ID_SIZE = 7 * 2
    SHEET_ID_FONT = "sans-serif"
    TRUE = "#ffffff"
    FALSE = "#000000"
    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self, data, sheet_id, group):
        """

        """
        self.data = data
        self.sheet_id = sheet_id
        self.group = group
        self.svg = ""

    def render_sheet(self):
        """
        
        """
        self.svg = ""
        self._render_sheet_rect()
        self._render_cells_rect()
        self._render_letters()
        self._render_cells()
        self._render_border()
        self.svg += "</g>\n"
        self._render_sheet_id()
        self.svg += "</g>\n"

        return self.svg

    def render_svg_sheet(self):
        """
        
        """
        self.svg += "<?xml version='1.0' encoding='utf-8'?>\n"
        self.svg += f"<svg viewBox='0 0 {self.sheet_width()} {self.sheet_height()}' xmlns='http://www.w3.org/2000/svg' fill='#000000'>\n"
        self.svg += self.render_sheet()
        self.svg += "</svg>"

        return self.svg

    def _render_sheet_rect(self):
        """
        
        """
        # sheet width = cells rect width + (cell_size * 2)
        sh = self.sheet_height()
        sbw = self.CELL_SIZE
        crs = self.cells_rect_size()
        sw = self.sheet_width()
        self.svg += f"<g transform='scale({self.SCALE})'>\n"
        self.svg += (f"<path d='M 0 0 V {sh} H {sbw} V {self.sheet_header_height() + sbw} "
                     f"H {sbw + crs} V {self.sheet_header_height() + sbw + crs} "
                     f"H {sbw} V {sh} H {sw} V {0} Z' fill='#000000' />")

    def _render_cells_rect(self):
        """
        
        """
        self.svg += (f"<g id='cells_rect' "
                     f"transform='translate({self.SHEET_BORDER_WIDTH},{self.SHEET_BORDER_WIDTH + self.sheet_header_height()})'>\n")
        
    def _render_border(self):
        """
        
        """
        self.svg += (f"<rect "
                     f"style='fill:#ffffff00; stroke-width:{self.WHITE_BORDER_WIDTH}; stroke:#ffffff; opacity:0' "
                     f"width='{self.cells_rect_size()}' "
                     f"height='{self.cells_rect_size()}' "
                     f"x='{0}' "
                     f"y='{0}'/>\n")

    def _render_letters(self):
        """
        
        """
        for i in range(26):
            l = self.LETTERS[i]
            self.svg += self._render_letter(self.LETS_LEFT_OFFSET,(i*24) + 18,l)
            self.svg += self._render_letter(self.LETS_RIGHT_OFFSET,(i*24) + 18,l)
            self.svg += self._render_letter((i*24) + 8,self.LETS_TOP_OFFSET,l)
            self.svg += self._render_letter((i*24) + 8,self.LETS_BOTTOM_OFFSET,l)

    def _render_letter(self, x, y, l):
        """
        
        """
        return (f"<text x='{x}' "
                f"y='{y}' "
                f"fill='#FFFFFF' "
                f"font-family='monospace' "
                f"font-size='14'>{l}</text>\n")

    def _render_cells(self):
        """
        
        """
        for x in range(26):
            for y in range(26):
                lx = self.LETTERS[x%26]
                ly = self.LETTERS[y%26]
                cell_data = self.data[f"{lx}{ly}"][self.group]
                females = ""
                if cell_data:
                    for pair in cell_data:
                        pair.sort()
                    cell_data = [f"{pair[0]}{pair[1]}" for pair in cell_data]
                    cell_data = list(set(cell_data))
                    females = ','.join(cell_data)
                    fill = "#ffffff00"
                    opacity = '0'
                else:
                    fill = "#000000ff"
                    opacity = '1'
                self.svg += (f"<rect id='{lx}{ly}' "
                             f"females='{females}' "
                             f"style='fill:{fill};fill-opacity:{opacity};stroke:#000000;stroke-width:{self.CELL_BORDER_WIDTH}' "
                             f"width='{self.CELL_SIZE}' "
                             f"height='{self.CELL_SIZE}' "
                             f"x='{(x*self.CELL_SIZE) + (self.CELL_BORDER_WIDTH / 2)}' "
                             f"y='{(y*self.CELL_SIZE) + (self.CELL_BORDER_WIDTH / 2)}'/>\n")

    def _render_sheet_id(self):
        """
        
        """
        self.svg += (f"<text id='sheet_id' "
                     f"x='32' "
                     f"y='18' "
                     f"fill='#FFFFFF' "
                     f"font-family='monospace' "
                     f"font-size='14'>{self.sheet_id}</text>\n")

    @classmethod
    def cells_rect_size(cls):
        """

        """
        return (cls.CELL_SIZE  * 26) + cls.CELL_BORDER_WIDTH

    @classmethod
    def sheet_header_height(cls):
        """
        
        """
        return cls.CELL_SIZE - cls.CELL_BORDER_WIDTH

    @classmethod
    def sheet_width(cls):
        """

        """
        return cls.cells_rect_size() + (cls.CELL_SIZE * 2)

    @classmethod
    def sheet_height(cls):
        """

        """
        return cls.sheet_width() + cls.sheet_header_height()