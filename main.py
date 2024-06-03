def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

#konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], 500, 500)


#pętla gry
window_open = True
while window_open:
    # pętla zdarzeń
    #screen.fill(LIGHTGREEN)
    screen.blit(BACKGROUND, [-300, -300])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        if event.type == pygame.QUIT:
            window_open = False

    # rysowanie i aktualizacja obiektów
    player.draw(screen)

    # aktualizacja okna gry
    pygame.display.flip()

    clock.tick(60)


pygame.quit()

#Komentarz







