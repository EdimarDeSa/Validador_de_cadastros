from tkinter import Entry


class PlaceHolderEntry(Entry):
    def __init__(self, placeholder="Texto padrão", placeholdercolor='gray30', **kw):
        super().__init__(**kw)

        self.placeholder = placeholder
        self.placeholder_color = placeholdercolor
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.set_placeholder()

    def set_placeholder(self):
        self.insert(0, self.placeholder)
        self.configure(fg=self.placeholder_color)

    def on_focus_in(self, _):
        if self['fg'] == self.placeholder_color:
            self.delete(0, 'end')
            self['fg'] = self.default_fg_color

    def on_focus_out(self, _):
        if not self.get():
            self.set_placeholder()
