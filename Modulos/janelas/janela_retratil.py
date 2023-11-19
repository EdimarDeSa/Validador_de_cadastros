from ttkbootstrap import Button, Frame, Label
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.style import Bootstyle

from Modulos.constants import *
from Modulos.imagens import *

__all__ = ['CollapsingFrame']


class CollapsingFrame(ScrolledFrame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        self.images = Imagens()

    def add(self, child, title='', bootstyle=PRIMARY, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return

        style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = Frame(self, bootstyle=style_color)
        frm.grid(row=self.cumulative_rows, column=0, sticky=EW)

        # header title
        header = Label(master=frm, text=title, bootstyle=(style_color, INVERSE))
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=LEFT, fill=BOTH, padx=10)

        # header toggle button
        def _func(c=child) -> any:
            return self._toggle_open_close(c)

        btn = Button(
            master=frm,
            image=self.images.img_seta_para_cima,
            bootstyle=style_color,
            command=_func,
        )
        btn.pack(padx=(0, 10), side=RIGHT)

        if kwargs.get('edita_sorteio'):
            edita_sorteio = kwargs.get('edita_sorteio')
            edit = Button(
                master=frm,
                image=self.images.img_editar,
                bootstyle=style_color,
                command=lambda c=child: edita_sorteio(c),
            )
            edit.pack(padx=(0, 10), side=RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images.img_seta_para_direita)
        else:
            child.grid()
            child.btn.configure(image=self.images.img_seta_para_cima)
