from fpdf import FPDF
import csv
from itertools import combinations

def set_font_by_lot(lot):
    if len(lot) < 3:
        pdf.set_font_size(size = 1200)
    elif len(lot) == 3:
        pdf.set_font_size(size = 1000)

def set_font_by_lines(lines):
    if lines == 1:
        pdf.set_font_size(size = 1200)
    elif lines == 2:
        pdf.set_font_size(size = 400)
    elif lines == 3:
        pdf.set_font_size(size = 400)
    elif lines == 4:
        pdf.set_font_size(size = 400)
    elif lines == 0:
        pdf.set_font_size(size = 175)

def set_font_by_chars(lot):
    if len(lot) < 3:
        pdf.set_font_size(size = 1200)
    elif len(lot) < 4:
        pdf.set_font_size(size = 1000)
    
def set_footnote_font():
    pdf.set_font_size(size = 175)
        
def set_page(row):
    if row[2] != '':
        print ('group')
    set_font(row[0])

def get_lot_row(index):
    return lot_list[index]
def get_lot_number(index):
    return lot_list[index][0]
def get_lot_group(index):
    return lot_list[index][1]
def get_lot_note(index):
    return lot_list[index][2]

height = 1080
width = 1920

pdf = FPDF(orientation='L', unit='pt', format=(height,width))
pdf.set_fill_color(0, 0, 0)
pdf.set_text_color(252, 255, 48)
pdf.set_font("Arial","B", size = 350)
pdf.set_margins(0, 0, 0)
pdf.set_auto_page_break(False, 0)

with open('import.csv', newline='') as csvfile:
    lot_list = list(csv.reader(csvfile))

length = len(lot_list)
i = 0

'''
#for 2 lines of text 5 chars per line
pdf.add_page()
pdf.set_font_size(size = 650)
pdf.multi_cell(0, height/2, txt = '', align = "C", fill = True)
'''



def write_to_slide(lot, footnote = ""):
    pdf.add_page()
    set_font_size(lot)
    cells = compute_cells(lot)
    if footnote != "":
        pdf.multi_cell(0, height/cells * .9, txt = lot, align = "C", fill = True)
        set_footnote_font()
        pdf.multi_cell(0, height * .1, txt = footnote, align = "C", fill = True)
    else:
        pdf.multi_cell(0, height/cells, txt = lot, align = "C", fill = True)
        
def set_font_size(lot):
    if len(lot) < 3:
        pdf.set_font_size(size = 1200)
    elif len(lot) < 4:
        pdf.set_font_size(size = 1000)
    elif len(lot) < 5:
        pdf.set_font_size(size = 800)
    elif len(lot) < 11:
        pdf.set_font_size(size = 600)

def compute_cells(lot):
    if len(lot) < 6:
        return 1
    elif len(lot) < 11:
        return 2


write_to_slide('1','this is a note')
write_to_slide('22','this is a note')
write_to_slide('333','this is a note')
write_to_slide('4444','this is a note')
write_to_slide('55555','this is a note')
write_to_slide('666666','this is a note')
write_to_slide('7777777','this is a note')
write_to_slide('88888888','this is a note')
write_to_slide('999999999','this is a note')




    

while i < length:
    print (lot_list[i][0])

    # create slide for group lots
    if lot_list[i][1] != "":
        count = 1 #counter to track number of lots in group
        group = get_lot_group(i) #identifier for lots in a group
        grouping = True #boolean var to continue looking for lots in a group
        group_list = [get_lot_row(i)] #list of all lots in a specific group
        
        while grouping:
            # get all lots of group
            if get_lot_group(i + 1) == group:
                count += 1
                i += 1
                group_list.append(get_lot_row(i))

            # after creating list of all group lots, process list to create slides
            else:
                lot_string = ""
                #make string of all lots in group
                for lots in group_list:
                    lot_string += lots[0]
                    lot_string += "/"

                # remove last newline char
                lot_string = lot_string[:-1]

                write_to_slide(lot_string)

                '''
                # slide with all lots of group listed
                pdf.add_page()
                #pdf.set_font_size(size = 50)
                set_font_by_lines(count)
                cell_height = height #/ count
                pdf.multi_cell(0, cell_height, txt = lot_string, align = "C", fill = True)
                '''

                # create slideds of all combinations of group
                # do for all combinations by decrementing count 
                while count > 1:
                    comb = combinations(group_list,count-1)
                    # create list of all combinations of current count
                    for lots in list(comb):

                    
                        #pdf.add_page()
                        #set_font_by_lines(count)
                        lot_string = ""
                        for lot in lots:
                            lot_string += lot[0] + "/"
                            # remove last newline char
                        lot_string = lot_string[:-1]
                        #cell_height = height #/ (count-1)
                        #pdf.multi_cell(0, cell_height, txt = lot_string, align = "C", fill = True)
                        
                        
                        write_to_slides(lot_string)
                        
                    count -= 1

                grouping = False

    # create slide for single lot
    else:
        
        pdf.add_page()
        set_font_by_chars(get_lot_number(i))
        if lot_list[i][2] != "":
            pdf.multi_cell(0, height*.9, txt = get_lot_number(i), align = "C", fill = True)
            set_footnote_font()
            pdf.multi_cell(0, height*.1, txt = lot_list[i][2], align = "C", fill = True)
        else:
            pdf.multi_cell(0, height, txt = get_lot_number(i), align = "C", fill = True)
            
    
    i += 1


pdf.output("demo.pdf")

    

'''
set_font(size = 620) for 2 chars 1 line

set_font(size = 500) for 3 chars 1 line

-----------------------------------------
for two lines
font size = 350
multi_cell(0, 90, txt, align c)
-----------------------------------------

2-d array in python
array - [[0 for i in range(cols)] for j in range(rows)]

'''

'''
array = [[0 for i in range(2)] for j in range(3)]
array[0][0] = 100
array[1][0] = 200
array[2][0] = 300
'''



'''
for lots in group_list:
print(lots)
'''
'''    
#count = 0
for row, lot in enumerate(lot_list):
    print (lot[0])
    #print(row)
    #count = 0
    i = row
    
    if lot[1] != '':
        count = 1;
        group = lot[1]
        grouping = True    
        while grouping:
            if lot_list[i+1][1] == group:
                i += 1
                count += 1
            else:
                grouping = False
       if count == print ("Count {}".format(count))
    
'''    


'''    
for row in lot_list:
    print (row[0])
    count = 0
    if row[1] != '':
        counter = 
        group = row[1]
        print (group)
        while 
        
    #pdf.set_font_size(set_font(row[0]))
    set_font(row[0])
    pdf.add_page()
    pdf.multi_cell(0, 240, txt = row[0], align = "C")
'''
    

#for row in data:
#    print(row)


#pdf.add_page()
