import pygame


class Button:
    """
    Clase para crear botones interactivos en el menú.
    """

    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        """
        Dibuja el botón con un diseño más elegante
        """
        # Dibujar el botón principal
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=2)

        # Agregar borde sutil
        border_color = (100, 100, 100)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=2)

        # Mejorar el texto
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.text, True, (220, 220, 220))
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Agregar sombra al texto
        shadow_surface = font.render(self.text, True, (20, 20, 20))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        screen.blit(shadow_surface, shadow_rect)

        # Dibujar el texto principal
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Maneja los eventos del botón
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False
