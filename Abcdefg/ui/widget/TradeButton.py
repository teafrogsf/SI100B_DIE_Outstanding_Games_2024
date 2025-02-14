import Config
from ui.widget.ClassicButton import ClassicButton


class TradeButton(ClassicButton):

    def __init__(self, text, pos, size, trade_option, bg_color=(0, 0, 0, 150), text_color=(255, 255, 255),
                 on_click=lambda: None, border_color=(0, 0, 0, 150), hover_bg_color=(0, 0, 0, 200),
                 hover_text_color=(255, 255, 255), inactive_bg_color=(0, 0, 0, 255), inactive_text_color=(50, 50, 50),
                 border_radius=8):
        super().__init__(text, pos, size, bg_color, text_color, on_click, border_color, hover_bg_color,
                         hover_text_color, inactive_bg_color, inactive_text_color, border_radius)
        self.trade_option = trade_option

    def on_toggle_click(self):
        text = self.on_click() or None
        if text is not None:
            Config.CLIENT.open_message_box(text, Config.CLIENT.current_ui)
        self.active &= self.trade_option.available

    def render_text(self, screen, text_color):
        render_coin = self.trade_option.price > 0
        text_surface = Config.FONT.render(self.text.get(), True, text_color)
        delta = 1 if self.mouse_down else 0
        text_rect = text_surface.get_rect(center=(self.rect.center[0] + delta, self.rect.center[1]
                                                  + (-10 if render_coin else 0) + delta))
        screen.blit(text_surface, text_rect)
        if render_coin:
            text_surface = Config.FONT.render(f"x{self.trade_option.price}", True, (255, 175, 45))
            text_rect = text_surface.get_rect(center=(
                self.rect.center[0] + 12 + delta, self.rect.center[1] + 10 + delta))
            screen.blit(text_surface, text_rect)
            screen.blit(Config.COIN_IMAGE, (self.rect.center[0] - 30 + delta, self.rect.center[1] + delta))
