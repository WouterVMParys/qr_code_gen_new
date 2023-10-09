import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os


class StreamlitEngine:

    def __init__(self):
        if 'nieuwe_namen' not in st.session_state:
            st.session_state['nieuwe_namen'] = []
        if 'qr_file_names' not in st.session_state:
            st.session_state['qr_file_names'] = []
        if 'success' not in st.session_state:
            st.session_state['success'] = "Bestand nog niet aangemaakt"

        self.add_new_member()
        st.markdown('#')
        self.create_project_overview()
        st.markdown('#')
        st.button("Maak qr codes", on_click=do_everything, args=(st.session_state['nieuwe_namen'],))
        st.write(st.session_state['success'])
        with open('qr_sheets/qr_document_from_streamlit_1.png', "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name="flower.png",
                mime="image/png"
            )

    def add_new_member(self):
        a, b, c, d = st.columns([3, 3, 3, 2])
        with a:
            voornaam = st.text_input('Voornaam','')
        with b:
            achternaam = st.text_input('Achternaam','')
        with c:
            groep = st.selectbox('Groep', ('U6', 'U8', 'U14', 'Jun&Sen', 'Recr', 'Wedstrplg'))
        with d:
            st.write('#')
        st.button('voeg toe', on_click=self.add_name_to_list, args=(voornaam, achternaam, groep))

    def add_name_to_list(self, vn, an, gr):
        st.session_state['nieuwe_namen'].append([vn, an, gr])
        st.session_state['success'] = "Bestand nog niet aangemaakt"

    def create_project_overview(self):
        with st.expander("Huidig overzicht"):
            a, b, c, d, e = st.columns([1, 4, 4, 3, 2])
            with a:
                st.write(':blue[**#**]')
            with b:
                st.write(':blue[**Voornaam**]')
            with c:
                st.write(':blue[**Achternaam**]')
            with d:
                st.write(':blue[**Groep**]')
            for i, k in enumerate(st.session_state['nieuwe_namen']):
                num, a, b, c, d = st.columns([1, 4, 4, 3, 2])
                with num:
                    st.write(i+1)
                with a:
                    st.write(k[0])
                with b:
                    st.write(k[1])
                with c:
                    st.write(k[2])
                with d:
                    butt = st.button("remove", key=k[0] + k[1] + '_rem_but', on_click=self.delete_name_from_list, args=(i,))

    def delete_name_from_list(self, ind):
        st.session_state['nieuwe_namen'].pop(ind)
        st.session_state['success'] = "Bestand nog niet aangemaakt"


def do_everything(name_list_in):
    if 'qr_sheet' not in st.session_state:
        st.session_state['qr_sheet'] = None

    member_list = [k[0] + " " + k[1] + " - " + k[2] for k in name_list_in]
    load_name_list_and_create_qrpng(member_list)
    create_qr_sheet_to_print()
    st.session_state['success'] = 'bestand klaar voor download'


def load_name_list_and_create_qrpng(name_list_in):
    if isinstance(name_list_in, list):
        print('found a list')
        for n in name_list_in:
            create_png_qr_with_logo(n)
    else:
        print(type(name_list_in))


def create_png_qr_with_logo(name_in):
    # taking image which user wants in the QR code center
    Logo_link = 'logo_bol.jpg'
    logo = Image.open(Logo_link)

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), PIL.Image.LANCZOS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    # adding URL or text to QRcode
    additional_chars = 18 - len(name_in)
    additional_chars = max(0, additional_chars)
    add_string = ''
    print('will have to add amount of spaces:', additional_chars)
    for i in range(additional_chars):
        add_string += ' '
    QRcode.add_data(name_in + '     ')

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = (0, 0, 100)

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    # save the QR code generated
    QRimg.save("qr_codes/" + name_in + ".png")

    print('QR code generated for ' + name_in + "!")
    file_str = name_in + ".png"
    if file_str not in st.session_state['qr_file_names']:
        print("ADDED {} to session state".format(file_str))
        st.session_state['qr_file_names'].append(file_str)
    else:
        print("{} already session state".format(file_str))


def black_bg_square(x_am, y_am, width, height, border):
    size = (width*x_am+border*2, height*y_am+border*2)
    paper_layer = Image.new('RGB', size, (255, 255, 255))
    print("created a big black screen with size: ", size)
    return paper_layer


def create_qr_sheet_to_print():
    max_x_amount = 4
    max_y_amount = 3
    if len(st.session_state['qr_file_names']) > 12:
        max_y_amount = 6
    current_x = 0
    current_y = 0
    border = 40
    x_step = 370
    y_step_text = 30
    y_step_text_overlap = 30
    y_step_qr = 370
    y_step = y_step_qr + y_step_text - y_step_text_overlap
    paper_layer = black_bg_square(max_x_amount, max_y_amount, x_step, y_step, border)
    full_cards_paper = paper_layer.copy()
    path_to_qr_files = 'qr_codes/'
    # qr_list = os.listdir(path_to_qr_files)
    # qr_list.sort()
    page_number = 1
    counter = 0
    # new_qr_list = [f_name for f_name in qr_list if f_name in st.session_state['qr_file_names']]
    print("QR FILE NQMES IN ST:", st.session_state['qr_file_names'])
    for qr_file in st.session_state['qr_file_names']:
        if counter > 23:
            full_cards_paper.save('qr_sheets/qr_document_from_streamlit_' + str(page_number) + '.png', quality=95)
            page_number += 1
            full_cards_paper = paper_layer.copy()
            counter = 0
            current_x = 0
            current_y = 0
        im1 = Image.open(path_to_qr_files + qr_file)
        im1 = im1.resize((370, 370))
        full_cards_paper.paste(im1, (current_x*x_step+border, current_y*y_step+border))

        name_font = ImageFont.truetype('fonts/OpenSans-Regular.ttf', int(20))
        text_to_insert = qr_file[:-4]

        size = (370, 30)
        text_image = Image.new('RGB', size, (255, 255, 255))
        image_editable = ImageDraw.Draw(text_image)
        image_editable.text((185-int(len(text_to_insert)/2)*10, 0), text_to_insert, (0, 0, 135), font=name_font)

        full_cards_paper.paste(text_image, (current_x*x_step+border, current_y*y_step + y_step_qr - y_step_text_overlap + border))
        current_x += 1
        if current_x >= max_x_amount:
            current_x = 0
            current_y += 1
        counter += 1

    full_cards_paper.save('qr_sheets/qr_document_from_streamlit_' + str(page_number) + '.png', quality=95)
    print("should be printed:", 'qr_sheets/qr_document_from_streamlit_' + str(page_number) + '.png')


if __name__ == "__main__":
    stEngine = StreamlitEngine()
