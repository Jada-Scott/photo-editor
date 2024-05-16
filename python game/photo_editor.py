import pygame
import cv2 as cv
import numpy as np
import random
from tkinter import filedialog
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray

class PhotoEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1300, 975])
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Photo Editor")
        self.x_center = self.screen.get_width() / 2
        self.y_center = self.screen.get_height() / 2
        self.pic_size = 475
        self.DEFAULT_IMAGE_SIZE = (self.pic_size, self.pic_size)
        self.DEFAULT_IMAGE1_LOC = self.x_center - self.pic_size * 1.2, self.y_center - self.pic_size * 0.95
        self.DEFAULT_IMAGE2_LOC = self.x_center + self.pic_size * 0.2, self.y_center - self.pic_size * 0.95
        self.black = (0,0,0)
        self.white = (255, 255, 255)
        self.gray = (165, 168, 173)
        self.running = True

        self.before_rect = pygame.Rect((self.x_center - self.pic_size * 1.2, self.y_center - self.pic_size * 0.95, self.pic_size, self.pic_size))
        self.after_rect = pygame.Rect((self.x_center + self.pic_size * 0.2, self.y_center - self.pic_size * 0.95, self.pic_size, self.pic_size))
        self.control_rect = pygame.Rect((4, 640, self.screen.get_width() - 10, 325))

        self.before_pic = pygame.draw.rect(self.screen, self.black, self.before_rect)
        self.after_pic = pygame.draw.rect(self.screen, self.black, self.after_rect)
        self.control_panel = pygame.draw.rect(self.screen, self.gray, self.control_rect)

        self.slider = Slider(self.screen, 750, 800, 500, 30, min=0, max=100, step=.10, initial=0)
        self.output = TextBox(self.screen, 970, 700, 75, 60, fontSize=30)
        self.slider_value = 0
        self.output.disable()

        self.button = Button(self.screen, self.x_center - self.pic_size * 1.1, self.y_center + self.pic_size * 0.07, self.pic_size * .75, 80,
            text='Select File',fontSize=40,margin=20,inactiveColour=(195, 195, 195),hoverColour=(165, 165, 165),
            pressedColour=(102, 102, 102),radius=20, onClick=lambda: self.file_select())

        self.buttonArray = ButtonArray(self.screen, 20, 650, 700, 300, (3, 1), border=20, texts=('Frequency', 'Saturation', 'Edges'),
            colour=self.gray, onClicks=(lambda: self.user_click_frequency(), lambda: self.user_click_saturation(), lambda: self.user_click_edges())
        )

        self.image = None

    def file_select(self):
        filepath = filedialog.askopenfilename()
        self.image_cv = cv.imread(filepath)
        image_cv = cv.cvtColor(self.image_cv, cv.COLOR_BGR2RGB)
        pygame_image = pygame.image.frombuffer(image_cv.tobytes(), image_cv.shape[:2][::-1], "RGB")
        self.image1 = pygame.transform.scale(pygame_image, self.DEFAULT_IMAGE_SIZE)
        self.screen.blit(self.image1, self.DEFAULT_IMAGE1_LOC)
        self.image = pygame.transform.scale(pygame_image, self.DEFAULT_IMAGE_SIZE)
        self.screen.blit(self.image, self.DEFAULT_IMAGE2_LOC)

    def user_click_frequency(self):

        if self.image is not None:

            image2 = cv.cvtColor(np.array(self.image_cv), cv.COLOR_RGB2BGR)
            x = image2.shape[0]
            y = image2.shape[1]
            for i in range(x):
                for j in range(y):
                    if random.randint(0, 1) == 0:
                        r = random.randint(0, 255)
                        g = random.randint(0, 255)
                        b = random.randint(0, 255)
                        image2[i, j] = (r, g, b)

            pygame_img = pygame.image.frombuffer(image2.tobytes(), image2.shape[:2][::-1], "RGB")
            self.image = pygame.transform.scale(pygame_img, self.DEFAULT_IMAGE_SIZE)
            self.screen.blit(self.image, self.DEFAULT_IMAGE2_LOC)


    def user_click_saturation(self):

        if self.image is not None:

            cvimage = cv.cvtColor(np.array(self.image_cv), cv.COLOR_RGB2BGR)
            resized_image = cv.resize(cvimage, self.DEFAULT_IMAGE_SIZE)
            imghsv = cv.cvtColor(resized_image, cv.COLOR_BGR2HSV).astype("float32")

            h, s, v = cv.split(imghsv)
            sat_factor = self.slider_value / 100
            s = s * self.slider_value
            s = np.clip(s, 0, 255)
            imghsv = cv.merge([h, s, v])

            imgrgb = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)
            self.image = pygame.image.frombuffer(imgrgb.tobytes(), imgrgb.shape[:2][::-1], "RGB")
            self.image = pygame.transform.scale(self.image, self.DEFAULT_IMAGE_SIZE)
            self.screen.blit(self.image, self.DEFAULT_IMAGE2_LOC)


    def user_click_edges(self):

        if self.image is not None:

            cvimage = cv.cvtColor(np.array(self.image_cv), cv.COLOR_RGB2BGR);
            resized_image = cv.resize(cvimage, self.DEFAULT_IMAGE_SIZE)
            gray_img = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)

            img_blur = cv.GaussianBlur(gray_img, (3, 3), 0)

            # Sobel Edge Detection
            sobelx = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=1, dy=0,
                               ksize=5)
            sobely = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=0, dy=1,
                               ksize=5)
            sobelxy = cv.Sobel(src=img_blur, ddepth=cv.CV_64F, dx=1, dy=1,
                                ksize=5)

            adjusted_img = cv.Canny(img_blur, 0, self.slider_value)

            adjusted_img_rgb = cv.cvtColor(adjusted_img, cv.COLOR_GRAY2RGB)
            pygame_img = pygame.image.frombuffer(adjusted_img_rgb.tobytes(), adjusted_img_rgb.shape[:2][::-1], "RGB")
            self.image = pygame.transform.scale(pygame_img, self.DEFAULT_IMAGE_SIZE)
            self.screen.blit(self.image, self.DEFAULT_IMAGE2_LOC)

    def slider_control(self):
        pass


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.slider_value = self.slider.getValue()
            self.output.setText(round(self.slider_value, 2))

            pygame_widgets.update(event)
            pygame.display.update()
            pygame.display.flip()



if __name__ == "__main__":
    editor = PhotoEditor()
    editor.run()
