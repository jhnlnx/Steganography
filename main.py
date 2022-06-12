from PIL import Image


def str_to_bool(i)->bool:
    return  True if i =='1' else False
     


def encode_LSB(src:str, msg:str,dst:str) -> bool:


    bin_array = list(map(str_to_bool,''.join([bin(ord(i))[2:].rjust(8,'0') for i in msg])))
    bin_array+=[False,False,False,False,False,False,False,False] # add null character as string delimter
    # Start encoding
    with Image.open(dst) as src_image:
        image_data = src_image.copy()

        bitmap = image_data.getdata()
        if len(bin_array) > len(bitmap):
            print("Messgae is too long for this image. Cannot fit in the image")
            return False

        width = image_data.size[0]
        x = 0
        y = 0

        for i in range(len(bin_array)):
            bits = list(bitmap[i])
            bits[0] = bits[0]>>1<<1  # shift right and left by one bit (eg 1001 -> 1000)
            if bin_array[i]:
                bits[0]+=1

            image_data.putpixel((x,y),tuple(bits))
            x  += 1
            if x == width:
                x = 0
                y += 1

        image_data.save(dst)

    return True 




def decode_LSB(src:str) -> str:
    with Image.open(src) as image_data:
        bitmap = image_data.getdata()
        msg = ""
        for i in range(0,len(bitmap),8):
            dec_byte=[]
            for j in range(8):
                pixel = bitmap[i+j][0]
                dec_byte.append(pixel>>1<<1 != bitmap[i+j][0])

            if True not in dec_byte : # End of string
                return msg
            msg += chr(int(''.join('1' if i else '0' for i in dec_byte), 2))
            
    return msg 

        

def test_diff( origin:str, encoded:str, bit_len:int = 8*20)-> None:
    buff_one = []
    buff_two = []

       
    with Image.open(origin) as image_data:
        bitmap = image_data.getdata()
        for i in range(bit_len):
            buff_one.append(list(bitmap[i])[0])
    with Image.open(encoded) as image_data:
        bitmap = image_data.getdata()
        for i in range(bit_len):
            buff_two.append(list(bitmap[i])[0])
            
    print("Are the buffers same? "+str(buff_two == buff_one))
    print(buff_one)
    print(buff_two)        

def main():
    encode_LSB('./src.png','My Test of secret msg you should see.\nDeveloper','./encoded.png')
    print(decode_LSB('./encoded.png'))
    #test_diff('./src.png','./encoded.png', bit_len = 10*8)
if __name__ == "__main__":
    main()
