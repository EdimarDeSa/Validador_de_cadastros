from pathlib import Path

from ttkbootstrap import PhotoImage


class Imagens:
    def __init__(self):
        self.BASE = (Path(__file__).resolve().parent.parent / "icons")

        self.img_lupa = self._abre_imagem("icons8-magnifier-24.png")
        self.img_borracha = self._abre_imagem("icons8-erase-24.png")
        self.img_editar = self._abre_imagem("icons8-edit-24.png")
        self.img_seta_para_direita = self._abre_imagem("icons8-double-right-24.png")
        self.img_seta_para_cima = self._abre_imagem("icons8-double-up-24.png")

    def _abre_imagem(self, nome_da_imagem: str) -> PhotoImage:
        return PhotoImage(file=self.BASE / nome_da_imagem)
