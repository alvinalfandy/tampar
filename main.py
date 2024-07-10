import pygame
import time
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Judul jendela
pygame.display.set_caption("Tampar Lyrics with Rain Effect")

# Warna
white = (255, 255, 255)
blue = (30, 144, 255)

# Font dan ukuran
font = pygame.font.SysFont(None, 48)

# Lirik lagu dan waktu jeda
lines = [
    {"text": "Hujan samarkan derasnya", "char_delay": 0.1},
    {"text": "Tutup air mata", "char_delay": 0.1},
    {"text": "Temani kecewaku yang telah lama", "char_delay": 0.11},
    {"text": "Berdosa kah ku berdoa", "char_delay": 0.1},
    {"text": "Minta kau terluka", "char_delay": 0.11},
    {"text": "Dan tinggalkan dirinya", "char_delay": 0.11},
    {"text": "Hujan samarkan derasnya", "char_delay": 0.11},
    {"text": "Tutup air mata", "char_delay": 0.14},
    {"text": "Tiga tahun tak terasa", "char_delay": 0.12},
    {"text": "Masih kau yang ada", "char_delay": 0.12},
    {"text": "Bodoh yang sebenarnya", "char_delay": 0.12},
    {"text": "Tampar aku di pipi", "char_delay": 0.12},
    {"text": "Sadarkan kau aku takkan terjadi", "char_delay": 0.12},
]

delays = [
    0.6, 0.6, 0.5, 1.6,
    0.6, 0.7, 0.7, 1.4,
    0.7, 0.5, 0.5, 3.6,
    0.5, 0.6, 0.6, 0.6,
    0.8, 0.9, 0.9, 0.8,
    0.8, 0.9, 0.9, 16.0,
    1.4, 0.9, 0.9, 0.8,
    0.8, 0.6, 0.5, 0.5,
    0.6, 5.0,
]

# Fungsi untuk menampilkan teks di tengah layar
def draw_text_centered(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Membuat efek hujan dengan gambar
class Rain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rain_img
        self.rect = self.image.get_rect()
        self.speedx = 3
        self.speedy = random.randint(5, 25)
        self.rect.x = random.randint(-100, screen_width)
        self.rect.y = random.randint(-screen_height, -5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > screen_height:
            self.rect.x = random.randint(-100, screen_width)
            self.rect.y = random.randint(-screen_height, -5)

# Inisialisasi gambar hujan, awan, dan karakter
try:
    rain_img = pygame.image.load('hujan.png')
    cloud_img = pygame.image.load('cloud.png')
    character_img = pygame.image.load('sadman.png')
except pygame.error as e:
    print(f"Could not load image: {e}")
    pygame.quit()
    exit()

character_rect = character_img.get_rect(center=(screen_width // 2, screen_height - 50))

# Membuat grup sprite hujan
rain_group = pygame.sprite.Group()

for i in range(100):
    rain = Rain()
    rain_group.add(rain)

# Loop utama
running = True
index = 0
char_index = 0
start_time = time.time()
end_of_lyrics = False
current_char_delay = lines[0]["char_delay"]
current_delay = delays[0]

# Mengatur kecepatan frame
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(blue)

    # Update dan gambar tetesan hujan
    rain_group.update()
    rain_group.draw(screen)

    # Gambar awan di kiri dan kanan
    screen.blit(cloud_img, (0, 0))  # Awan di kiri
    screen.blit(cloud_img, (screen_width - cloud_img.get_width(), 0))  # Awan di kanan

    if not end_of_lyrics:
        if index < len(lines):
            line = lines[index]
            if char_index < len(line["text"]):
                draw_text_centered(line["text"][:char_index + 1], font, white, screen, screen_width // 2, screen_height // 2)
                current_char_delay -= dt
                if current_char_delay <= 0:
                    char_index += 1
                    current_char_delay = line["char_delay"]
            else:
                current_delay -= dt
                if current_delay <= 0:
                    index += 1
                    char_index = 0
                    if index < len(lines):
                        current_char_delay = lines[index]["char_delay"]
                        current_delay = delays[index] if index < len(delays) else 0.5
                    else:
                        end_of_lyrics = True
        else:
            end_of_lyrics = True
            draw_text_centered("End of Lyrics", font, white, screen, screen_width // 2, screen_height // 2)
    else:
        draw_text_centered("End of Lyrics", font, white, screen, screen_width // 2, screen_height // 2)

    # Gambar karakter sedih di bawah layar
    screen.blit(character_img, character_rect)

    pygame.display.flip()

pygame.quit()
