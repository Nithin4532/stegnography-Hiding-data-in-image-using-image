from tkinter import *
from tkinter import filedialog, messagebox, font as tkFont
from PIL import Image, ImageTk
from io import BytesIO
import os

class Stegno:
    output_image_size = 0

    def main(self, root):
        root.title('Team_Unity_Steganography')
        root.geometry('500x600')
        root.resizable(width=TRUE, height=TRUE)
        f = Frame(root)
        custom_font = tkFont.Font(family="Poppins", size=24)
        title = Label(f, text='Select one', font=custom_font)
        title.grid(pady=10)

        b_encode = Button(f, text="Encode", command=lambda: self.frame1_encode(f), font=custom_font, padx=20, pady=10)
        b_encode.grid(pady=20)
        b_decode = Button(f, text="Decode", command=lambda: self.frame1_decode(f), font=custom_font, padx=20, pady=10)
        b_decode.grid(pady=20)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        f.grid()
        title.grid(row=1)
        b_encode.grid(row=2)
        b_decode.grid(row=3)

    def home(self, frame):
        frame.destroy()
        self.main(root)

    def frame1_decode(self, f):
        f.destroy()
        d_f2 = Frame(root)
        
        custom_font = tkFont.Font(family="Poppins", size=24)
        l1 = Label(d_f2, text='Select Image with Hidden Text:',font=custom_font)
        l1.grid(pady=10)
        bws_button = Button(d_f2, text='Select', command=lambda: self.frame2_decode(d_f2),font=custom_font, padx=20, pady=10)
        bws_button.grid(pady=20)
        back_button = Button(d_f2, text='Cancel', command=lambda: self.home(d_f2),font=custom_font, padx=20, pady=10)
        back_button.grid(pady=20)
        d_f2.grid()

    def frame2_decode(self, d_f2):
        d_f3 = Frame(root)
        myfile = filedialog.askopenfilename(filetypes=[('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l4 = Label(d_f3, text='Selected Image:')
            l4.grid(pady=10)
            panel = Label(d_f3, image=img)
            panel.image = img
            panel.grid()
            root.after(3000, lambda: self.show_decoded_data(d_f3, myimg))
            d_f3.grid(row=1)
            d_f2.destroy()

    def show_decoded_data(self, d_f3, myimg):
        hidden_data = self.decode(myimg)
        l2 = Label(d_f3, text='Hidden Data:')
        l2.grid(pady=10)
        text_area = Text(d_f3, width=50, height=10)
        text_area.insert(INSERT, hidden_data)
        text_area.configure(state='disabled')
        text_area.grid()
        back_button = Button(d_f3, text='Cancel', command=lambda: self.home(d_f3))
        back_button.grid(pady=10)

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())
        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                binstr += '0' if i % 2 == 0 else '1'
            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def frame1_encode(self, f):
        f.destroy()
        f2 = Frame(root)
        custom_font = tkFont.Font(family="Poppins", size=24)
        l1 = Label(f2, text='Select the Image to Hide Text:',font=custom_font)
        l1.grid(pady=10)
        bws_button = Button(f2, text='Select', command=lambda: self.frame2_encode(f2),font=custom_font, padx=20, pady=10)
        bws_button.grid(pady=10)
        back_button = Button(f2, text='Cancel', command=lambda: self.home(f2),font=custom_font, padx=20, pady=10)
        back_button.grid(pady=10)
        f2.grid()

    def frame2_encode(self, f2):
        ep = Frame(root)
        myfile = filedialog.askopenfilename(filetypes=[('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((300, 200))
            img = ImageTk.PhotoImage(myimage)
            l3 = Label(ep, text='Selected Image:')
            l3.grid(pady=10)
            panel = Label(ep, image=img)
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            l2 = Label(ep, text='Enter the message:')
            l2.grid(pady=10)
            text_area = Text(ep, width=50, height=10)
            text_area.grid()
            encode_button = Button(ep, text='Cancel', command=lambda: self.home(ep))
            encode_button.grid(pady=10)
            back_button = Button(ep, text='Encode', command=lambda: [self.enc_fun_with_delay(text_area, myimg), self.home(ep)])
            back_button.grid(pady=10)
            ep.grid(row=1)
            f2.destroy()

    def enc_fun_with_delay(self, text_area, myimg):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            newimg.save(filedialog.asksaveasfilename(initialfile=temp, filetypes=[('png', '*.png')], defaultextension=".png"))
            
            root.after(3000, lambda: messagebox.showinfo("Success", "Encoding Successful"))

    def genData(self, data):
        newd = []
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    if pix[j] != 0:
                        pix[j] -= 1
                    else:
                        pix[j] += 1
            if i == lendata - 1:
                if pix[-1] % 2 == 0:
                    if pix[-1] != 0:
                        pix[-1] -= 1
                    else:
                        pix[-1] += 1
            else:
                if pix[-1] % 2 != 0:
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

root = Tk()
o = Stegno()
o.main(root)
root.mainloop()
