from fpdf import FPDF
import csv
from itertools import combinations
    
def set_footnote_font():
    pdf.set_font_size(size = 125)
    
def write_to_slide(lot_line):
    pdf.add_page()
    lot_number = get_lot_number(lot_line)
    lot_footnote = get_lot_footnote(lot_line)
    set_font_size(lot_number)
    cells = compute_cells(lot_number)
    if lot_footnote != "":
        pdf.multi_cell(0, height/cells * .9, txt = lot_number, align = "C", fill = True)
        set_footnote_font()
        pdf.multi_cell(0, height * .1, txt = lot_footnote, align = "C", fill = True)
    else:
        pdf.multi_cell(0, height/cells, txt = lot_number, align = "C", fill = True)
        
def write_all_to_slide(lot_string, footnote):
    pdf.add_page()
    set_font_size(lot_string)
    cells = compute_cells(lot_string)
    if footnote != "":
        pdf.multi_cell(0, height/cells * .9, txt = lot_string, align = "C", fill = True)
        set_footnote_font()
        pdf.multi_cell(0, height * .1, txt = footnote, align = "C", fill = True)
    else:
        pdf.multi_cell(0, height/cells, txt = lot_string, align = "C", fill = True)
        
def set_font_size(lot):
    slash_count = lot.count('/')
    if slash_count == 2 and len(lot) < 6:
        pdf.set_font_size(size = 800)
    elif len(lot) < 3:
        pdf.set_font_size(size = 1200)
    elif len(lot) < 4:
        pdf.set_font_size(size = 1000)
    elif len(lot) < 5:
        pdf.set_font_size(size = 800)
    elif len(lot) < 11:
        pdf.set_font_size(size = 600)
    elif len(lot) < 16:
        pdf.set_font_size(size = 500)
def compute_cells(lot):
    if len(lot) < 6:
        return 1
    elif len(lot) < 11:
        return 2
    elif len(lot) < 16:
        return 2

def get_lot_row(index):
    return lot_list[index]
def get_lot_number(index):
    return lot_list[index][0]
def get_lot_group(index):
    return lot_list[index][1]
def get_lot_note(index):
    return lot_list[index][2]
def get_lot_number(lot_line):
    return lot_line[0]
def get_lot_group(lot_line):
    return lot_line[1]
def get_lot_footnote(lot_line):
    return lot_line[2]
def correct_formatting (lot_string):
    if lot_string.count("/") == 1 and len(lot_string) == 7:
        index = lot_string.find("/") + 1
        new_lot_string = lot_string[:index] + "\n" + lot_string[index:]
        return new_lot_string
    else:
        return lot_string


# the size of the pdf doc in pts
height = 1080
width = 1920

# prep pdf doc
pdf = FPDF(orientation='L', unit='pt', format=(height,width))
pdf.set_fill_color(0, 0, 0)
pdf.set_text_color(252, 255, 48)
pdf.set_font("Arial","B", size = 350)
pdf.set_margins(0, 0, 0)
pdf.set_auto_page_break(False, 0)

# open the csv file of lot info
with open('import.csv', newline='') as csvfile:
    lot_list = list(csv.reader(csvfile))

length = len(lot_list)
i = 1 #start at index 1 since row 1 of csv is column headers

while i < length:
    # create slide for group lots
    group = get_lot_group(lot_list[i])
    if group != "":
        count = 1 #counter to track number of lots in group
        grouping = True #boolean var to continue looking for lots in a group
        group_list = [lot_list[i]] #list of all lots in a specific group

        while grouping:
            if i != length - 1 and get_lot_group(lot_list[i+1]) == group:
                count += 1
                i += 1
                group_list.append(lot_list[i])
            else:
                lot_string = ""
                for lots in group_list:
                    lot_string += lots[0] + "/"
                lot_string = lot_string[:-1]
                lot_string = correct_formatting(lot_string)
                # write all of group to one slide
                write_all_to_slide(lot_string, group_list[0][2])

                # create slides for all combinations of group
                while count > 1:
                    comb = combinations(group_list, count - 1)
                    for lots in list(comb):
                        lot_string = ""
                        for lot in lots:
                            lot_string += lot[0] + "/"
                        lot_string = lot_string[:-1]
                        lot_string = correct_formatting(lot_string)
                        write_all_to_slide(lot_string, group_list[0][2])

                    count -= 1
                grouping = False
            
    # create slide for single lot
    else:
        write_to_slide(lot_list[i])
    
    i += 1


pdf.output("lot_slides.pdf")

    
