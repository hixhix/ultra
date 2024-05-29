from zygalski_sheets.zygalski_sheets_svg.svg_sheet import SVGZygalskiSheet
from enigma_core.validators.scrambler_validators.scrambler_validators import *
from zygalski_sheets.sheet_data import SheetDataGenerator
from collections import deque


class ZygalskiSheetSolution:

    TABLE_LETS_LEFT_OFFSET = 30
    TABLE_LETS_RIGHT_OFFSET = (SVGZygalskiSheet.CELL_SIZE * 83) + 3
    TABLE_LETS_TOP_OFFSET = 40
    TABLE_LETS_BOTTOM_OFFSET = (SVGZygalskiSheet.CELL_SIZE * 84) + 10
    WINDOW_LETS_LEFT_OFFSET = 19
    WINDOW_LETS_RIGHT_OFFSET = (SVGZygalskiSheet.CELL_SIZE * 28) + 18
    WINDOW_LETS_TOP_OFFSET = 29
    WINDOW_LETS_BOTTOM_OFFSET = (SVGZygalskiSheet.CELL_SIZE * 29) + 5
    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self):
        self.svg = ""
        self._rs = None

    def show_solution(self, machine_type, indicators, permutation, rs):
        """
        
        """
        self._machine_type = machine_type
        self._rs = rs
        self._make_translations()
        self.svg = "<?xml version='1.0' encoding='utf-8'?>\n"
        self.svg += f"<svg viewBox='0 0 {self._light_table_width()} {self._light_table_height()}' xmlns='http://www.w3.org/2000/svg' fill='#000000'>\n"
        self.svg += self._render_light_table()
        self._render_sheets(indicators, permutation)
        self.svg += self._render_window()
        self.svg += "</svg>"

        return self.svg
    
    def _make_translations(self):
        """
        
        """
        self._translations = {}
        offset = self.LETTERS.index(self._rs)
        lets = deque(self.LETTERS.copy())
        lets.rotate(offset)
        lets = list(lets)

        for i in range(26):
            c1 = self.LETTERS[i]
            c2 = lets[i]
            self._translations[c1] = c2

    def _render_sheets(self, indicators, permutation):
        """
        
        """
        letters = [chr(i) for i in range(65,91)]

        try:
            perm_dict = ScramblerValidators.valid_permutation_string(self._machine_type, permutation, rs_flag=False, group_flag=False)
        except PermutationError as e:
            raise e
        else:
            for indicator in indicators:
                settings = {
                    "SCRAMBLER_SETTINGS":{
                        "REFLECTOR_TYPE":perm_dict["REFLECTOR"],
                        "ROTOR_TYPES":{
                            "RS":perm_dict["RS_TYPE"],
                            "RM":perm_dict["RM_TYPE"],
                            "RF":perm_dict["RF_TYPE"]
                        },
                        "ROTOR_SETTINGS":{
                            "RS":self._translations[indicator[0]],
                            "RM":"A",
                            "RF":"A"
                        },
                        "RING_SETTINGS":{"RS":'A',"RM":"A","RF":"A"}
                    }
                }
                sheet_data_generator = SheetDataGenerator()
                sheet_data = sheet_data_generator.data(settings, self._machine_type)

                x, y = self._sheet_position(indicator[1], indicator[2])
                groups = self._get_groups(indicator)
                for group in groups:
                    sheet_generator = SVGZygalskiSheet(sheet_data, f"{indicator[0]}_{permutation}", group)
                    sheet = sheet_generator.render_sheet()

                    self.svg += f"<g transform='translate({x},{y})'>\n"
                    self.svg += sheet
                    self.svg += "</g>\n"

    def _render_window(self):
        """
        
        """
        x, y = self._window_position()
        window = ""
        window += f"<g transform='scale({SVGZygalskiSheet.SCALE}) translate({x} {y})'>\n"
        window += (f"<path d='M 0 0 "
                   f"V {self._window_size()} "
                   f"H {self._window_border_width()} "
                   f"V {self._window_border_width()} "
                   f"H {self._window_border_width() + self._window_rect_size()} "
                   f"V {self._window_border_width() + self._window_rect_size()} "
                   f"H {self._window_border_width()} "
                   f"V {self._window_size()} "
                   f"H {self._window_size()} "
                   f"V 0 "
                   f"Z' fill='#555555' />")
        
        window = self._render_window_numbers(window)

        window += "</g>\n"
        
        return window

    def _render_window_numbers(self, window):
        """
        
        """
        letters = self.LETTERS.copy()
        letters.reverse()
        for i in range(26):
            l = letters[i]
            window += self._render_letter(self.WINDOW_LETS_LEFT_OFFSET,(i*24) + 63,l)
            window += self._render_letter(self.WINDOW_LETS_RIGHT_OFFSET,(i*24) + 63,l)
            window += self._render_letter((i*24) + 56,self.WINDOW_LETS_TOP_OFFSET,l)
            window += self._render_letter((i*24) + 56,self.WINDOW_LETS_BOTTOM_OFFSET,l)

        return window

    def _render_light_table(self):
        """
        
        """
        table = ""
        table += f"<g transform='scale({SVGZygalskiSheet.SCALE})'>\n"
        table += (f"<path d='M 0 0 "
                  f"V {self._light_table_height()}"
                  f"H {self._light_table_border_width()}"
                  f"V {self._light_table_border_width()}"
                  f"H {self._light_table_border_width() + self._light_table_rect_width()} "
                  f"V {self._light_table_border_width() + self._light_table_rect_height()} "
                  f"H {self._light_table_border_width()} "
                  f"V {self._light_table_height()} "
                  f"H {self._light_table_width()} "
                  f"V 0 "
                  f"Z' fill='#000000' />")
        
        table = self._render_light_table_letters(table)

        table += "</g>\n"

        return table

    def _render_light_table_letters(self, table):
        """
        
        """
        letters = self.LETTERS.copy()
        letters.reverse()
        for i in range(26):
            l = letters[i]
            table += self._render_letter(self.TABLE_LETS_LEFT_OFFSET,((i+25)*24) + 136,l)
            table += self._render_letter(self.TABLE_LETS_LEFT_OFFSET,((i+51)*24) + 136,l)
            table += self._render_letter(self.TABLE_LETS_RIGHT_OFFSET,((i+25)*24) + 136,l)
            table += self._render_letter(self.TABLE_LETS_RIGHT_OFFSET,((i+51)*24) + 136,l)
            table += self._render_letter(((i+25)*24) + 105,self.TABLE_LETS_TOP_OFFSET,l)
            table += self._render_letter(((i+51)*24) + 105,self.TABLE_LETS_TOP_OFFSET,l)
            table += self._render_letter(((i+25)*24) + 105,self.TABLE_LETS_BOTTOM_OFFSET,l)
            table += self._render_letter(((i+51)*24) + 105,self.TABLE_LETS_BOTTOM_OFFSET,l)
        return table

    def _render_letter(self, x, y, l):
        """
        
        """
        return (f"<text x='{x}' "
                f"y='{y}' "
                f"fill='#ffffff' "
                f"font-family='monospace' "
                f"font-size='14'>{l}</text>\n")            

    def _light_table_border_width(self):
        """
        
        """
        return SVGZygalskiSheet.CELL_SIZE * 3

    def _light_table_width(self):
        """
        
        """
        return self._light_table_rect_width() + (self._light_table_border_width() * 2)

    def _light_table_height(self):
        """
        
        """
        return self._light_table_rect_height() + (self._light_table_border_width() * 2)
    
    def _light_table_rect_width(self):
        """
        
        """
        return SVGZygalskiSheet.sheet_width() + ((SVGZygalskiSheet.CELL_SIZE - SVGZygalskiSheet.CELL_BORDER_WIDTH)  * 27) + SVGZygalskiSheet.CELL_BORDER_WIDTH

    def _light_table_rect_height(self):
        """
        
        """
        return SVGZygalskiSheet.sheet_height() + ((SVGZygalskiSheet.CELL_SIZE - SVGZygalskiSheet.CELL_BORDER_WIDTH)  * 27) + SVGZygalskiSheet.CELL_BORDER_WIDTH
    
    def _window_size(self):
        """
        
        """
        return self._window_rect_size() + (self._window_border_width() * 2)
    
    def _window_rect_size(self):
        """
        
        """
        return SVGZygalskiSheet.cells_rect_size() / 2
    
    def _window_border_width(self):
        """
        
        """
        return SVGZygalskiSheet.CELL_SIZE * 2

    def _window_position(self):
        """
        
        """
        x = self._light_table_border_width() - (SVGZygalskiSheet.SHEET_BORDER_WIDTH * 2) + (SVGZygalskiSheet.cells_rect_size() / 2) + SVGZygalskiSheet.CELL_SIZE
        y = x + SVGZygalskiSheet.sheet_header_height()

        return x, y
    
    def _get_groups(self, indicator):
        """
    
        """
        groups = []

        if indicator[4] == indicator[7]:
            groups.append("G1")
        if indicator[5] == indicator[8]:
            groups.append("G2")
        if indicator[6] == indicator[9]:
            groups.append("G3")

        return groups

    def _sheet_position(self, xl, yl):
        """
        
        """
        x = (self._light_table_border_width() / 2) + (((25 * SVGZygalskiSheet.CELL_SIZE) - (self.LETTERS.index(xl) * SVGZygalskiSheet.CELL_SIZE)) * SVGZygalskiSheet.SCALE)
        y = (self._light_table_border_width() / 2) + (((25 * SVGZygalskiSheet.CELL_SIZE) - (self.LETTERS.index(yl) * SVGZygalskiSheet.CELL_SIZE)) * SVGZygalskiSheet.SCALE)

        return x, y
