import board
import neopixel

offsets = [10,0,3,0,6,8,4, 8,11,6,8,1,9,11, 9,6,7,1,10,8,8, 3,5,11,2,9,10,10, 6,5,0,4,3,8,8]

pixels = neopixel.NeoPixel(board.D18, 35 * 12, brightness=0.1, auto_write=False, pixel_order=neopixel.GRB)
for n in range(35):
  pixels[12*n + (11 + offsets[n]) % 12]=(255,0,0)
  pixels[12*n + (0 + offsets[n]) % 12]=(255,0,0)
  pixels[12*n + (1 + offsets[n]) % 12]=(0,255,0)
  pixels[12*n + (2 + offsets[n]) % 12]=(0,0,255)
pixels.show()
