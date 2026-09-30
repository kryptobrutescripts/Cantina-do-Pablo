import json
import sys
import shutil
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QScrollArea, QFrame, QMessageBox, QStackedWidget,
    QLineEdit, QInputDialog, QSizePolicy, QListWidget, QListWidgetItem,
    QComboBox, QFileDialog, QDialog, QFormLayout, QDoubleSpinBox
)
from PySide6.QtGui import (
    QPixmap, QDesktopServices, QFont, QPalette, QColor
)
from PySide6.QtCore import Qt, QUrl, QTimer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
v1 = Path(__file__).resolve().parent
v2 = v1 / "imagens"
v3 = v1 / "comandas"
v4 = 4
v5 = "admin"

# ----------------------------------------------------------------------
# Tema visual: dark + verde
# ----------------------------------------------------------------------
COR_FUNDO = "#080d0b"
COR_FUNDO_ALT = "#0b120f"
COR_SUPERFICIE = "#101915"
COR_SUPERFICIE_2 = "#15211b"
COR_SUPERFICIE_3 = "#1b2a23"
COR_BORDA = "#1e2e26"
COR_BORDA_FORTE = "#2b4136"
COR_TEXTO = "#e8f3ed"
COR_TEXTO_SUAVE = "#95ab9f"
COR_TEXTO_FRACO = "#62786c"
COR_VERDE = "#22c55e"
COR_VERDE_CLARO = "#4ade80"
COR_VERDE_PRESS = "#16a34a"
COR_VERDE_ESCURO = "#14532d"
COR_VERDE_TINT = "#0f2a1b"
COR_SOBRE_VERDE = "#04140a"
COR_PERIGO = "#f87171"
COR_PERIGO_FUNDO = "#2a1416"
COR_PERIGO_BORDA = "#5a2327"
COR_IMAGEM_FUNDO = "#eef3f0"
COR_IMAGEM_TEXTO = "#6b7f74"
FONTE_UI = '"Segoe UI", "Inter", "Helvetica Neue", Arial, sans-serif'
SETA_BAIXO = (v1 / "assets" / "seta_baixo.png").as_posix()


def estilo_btn_primario(tam=14, raio=10):
    return f"""
        QPushButton {{
            background: {COR_VERDE};
            color: {COR_SOBRE_VERDE};
            border: none;
            border-radius: {raio}px;
            padding: 0 20px;
            font-size: {tam}px;
            font-weight: bold;
        }}
        QPushButton:hover {{ background: {COR_VERDE_CLARO}; }}
        QPushButton:pressed {{ background: {COR_VERDE_PRESS}; }}
        QPushButton:disabled {{
            background: {COR_SUPERFICIE_3};
            color: {COR_TEXTO_FRACO};
        }}
    """


def estilo_btn_secundario(tam=14, raio=10):
    return f"""
        QPushButton {{
            background: {COR_SUPERFICIE_2};
            color: {COR_TEXTO};
            border: 1px solid {COR_BORDA_FORTE};
            border-radius: {raio}px;
            padding: 0 18px;
            font-size: {tam}px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: {COR_SUPERFICIE_3};
            border: 1px solid {COR_VERDE};
            color: {COR_VERDE_CLARO};
        }}
        QPushButton:pressed {{ background: {COR_VERDE_TINT}; }}
    """


def estilo_btn_perigo(tam=13, raio=10):
    return f"""
        QPushButton {{
            background: {COR_PERIGO_FUNDO};
            color: {COR_PERIGO};
            border: 1px solid {COR_PERIGO_BORDA};
            border-radius: {raio}px;
            padding: 0 18px;
            font-size: {tam}px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: #3a1a1d;
            border: 1px solid {COR_PERIGO};
        }}
    """


def estilo_btn_passo():
    return f"""
        QPushButton {{
            background: transparent;
            color: {COR_TEXTO};
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: {COR_SUPERFICIE_3};
            color: {COR_VERDE_CLARO};
        }}
    """


def estilo_marca(tam_fonte=24, raio=12):
    return f"""
        QLabel {{
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 {COR_VERDE_CLARO}, stop: 1 {COR_VERDE_PRESS}
            );
            color: {COR_SOBRE_VERDE};
            border-radius: {raio}px;
            font-size: {tam_fonte}px;
            font-weight: bold;
        }}
    """


def estilo_pilula(cor_texto=None):
    cor_texto = cor_texto or COR_TEXTO_SUAVE
    return f"""
        QLabel {{
            background: {COR_SUPERFICIE_2};
            border: 1px solid {COR_BORDA_FORTE};
            border-radius: 13px;
            padding: 4px 13px;
            font-size: 12px;
            font-weight: 600;
            color: {cor_texto};
        }}
    """


def espacar_letras(rotulo, px=1.5):
    fonte = rotulo.font()
    fonte.setLetterSpacing(QFont.AbsoluteSpacing, px)
    rotulo.setFont(fonte)


ESTILO_GLOBAL = f"""
    QWidget {{
        font-family: {FONTE_UI};
        font-size: 14px;
        color: {COR_TEXTO};
    }}
    QLabel {{ background: transparent; }}
    QWidget#janela {{ background: {COR_FUNDO}; }}
    QToolTip {{
        background: {COR_SUPERFICIE_3};
        color: {COR_TEXTO};
        border: 1px solid {COR_BORDA_FORTE};
        padding: 6px 10px;
    }}
    QMessageBox, QInputDialog {{ background: {COR_SUPERFICIE}; }}
    QMessageBox QLabel, QInputDialog QLabel {{
        color: {COR_TEXTO};
        font-size: 14px;
    }}
    QMessageBox QPushButton, QInputDialog QPushButton {{
        background: {COR_SUPERFICIE_2};
        color: {COR_TEXTO};
        border: 1px solid {COR_BORDA_FORTE};
        border-radius: 8px;
        padding: 8px 22px;
        min-width: 84px;
        font-weight: 600;
    }}
    QMessageBox QPushButton:hover, QInputDialog QPushButton:hover {{
        border: 1px solid {COR_VERDE};
        color: {COR_VERDE_CLARO};
    }}
    QMessageBox QPushButton:default, QInputDialog QPushButton:default {{
        background: {COR_VERDE};
        color: {COR_SOBRE_VERDE};
        border: 1px solid {COR_VERDE};
    }}
    QMessageBox QPushButton:default:hover, QInputDialog QPushButton:default:hover {{
        background: {COR_VERDE_CLARO};
        color: {COR_SOBRE_VERDE};
    }}
    QScrollArea {{ background: transparent; border: none; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}
    QScrollBar:vertical {{
        background: transparent;
        width: 12px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical {{
        background: {COR_BORDA_FORTE};
        border-radius: 4px;
        min-height: 40px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {COR_VERDE}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
        background: none;
        border: none;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 12px;
        margin: 2px;
    }}
    QScrollBar::handle:horizontal {{
        background: {COR_BORDA_FORTE};
        border-radius: 4px;
        min-width: 40px;
    }}
    QScrollBar::handle:horizontal:hover {{ background: {COR_VERDE}; }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
        background: none;
        border: none;
    }}
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
    }}
    QLineEdit, QDoubleSpinBox {{
        background: {COR_FUNDO_ALT};
        border: 1px solid {COR_BORDA_FORTE};
        border-radius: 8px;
        padding: 9px 12px;
        color: {COR_TEXTO};
        selection-background-color: {COR_VERDE_ESCURO};
        selection-color: {COR_TEXTO};
    }}
    QLineEdit:focus, QDoubleSpinBox:focus {{
        border: 1px solid {COR_VERDE};
    }}
    QLineEdit:read-only {{ color: {COR_TEXTO_SUAVE}; }}
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        width: 0px;
        border: none;
    }}
    QComboBox {{
        background: {COR_FUNDO_ALT};
        border: 1px solid {COR_BORDA_FORTE};
        border-radius: 8px;
        padding: 9px 12px;
        color: {COR_TEXTO};
    }}
    QComboBox:focus, QComboBox:on {{ border: 1px solid {COR_VERDE}; }}
    QComboBox::drop-down {{ border: none; width: 30px; }}
    QComboBox::down-arrow {{
        image: url("{SETA_BAIXO}");
        width: 12px;
        height: 8px;
    }}
    QComboBox QAbstractItemView {{
        background: {COR_SUPERFICIE_2};
        border: 1px solid {COR_BORDA_FORTE};
        color: {COR_TEXTO};
        selection-background-color: {COR_VERDE_ESCURO};
        selection-color: {COR_TEXTO};
        outline: none;
        padding: 4px;
    }}
    QListWidget {{
        background: {COR_SUPERFICIE};
        border: 1px solid {COR_BORDA};
        border-radius: 14px;
        padding: 6px;
        outline: none;
    }}
    QListWidget::item {{
        padding: 12px;
        border-radius: 8px;
        color: {COR_TEXTO_SUAVE};
    }}
    QListWidget::item:hover {{
        background: {COR_SUPERFICIE_2};
        color: {COR_TEXTO};
    }}
    QListWidget::item:selected {{
        background: {COR_VERDE_TINT};
        color: {COR_VERDE_CLARO};
    }}
"""


def aplicar_paleta_escura(app):
    paleta = QPalette()
    paleta.setColor(QPalette.Window, QColor(COR_FUNDO))
    paleta.setColor(QPalette.WindowText, QColor(COR_TEXTO))
    paleta.setColor(QPalette.Base, QColor(COR_FUNDO_ALT))
    paleta.setColor(QPalette.AlternateBase, QColor(COR_SUPERFICIE))
    paleta.setColor(QPalette.Text, QColor(COR_TEXTO))
    paleta.setColor(QPalette.Button, QColor(COR_SUPERFICIE_2))
    paleta.setColor(QPalette.ButtonText, QColor(COR_TEXTO))
    paleta.setColor(QPalette.ToolTipBase, QColor(COR_SUPERFICIE_3))
    paleta.setColor(QPalette.ToolTipText, QColor(COR_TEXTO))
    paleta.setColor(QPalette.PlaceholderText, QColor(COR_TEXTO_FRACO))
    paleta.setColor(QPalette.Highlight, QColor(COR_VERDE_ESCURO))
    paleta.setColor(QPalette.HighlightedText, QColor(COR_TEXTO))
    paleta.setColor(QPalette.Link, QColor(COR_VERDE_CLARO))
    app.setPalette(paleta)


def caixa_mensagem(pai, titulo, texto, botoes=QMessageBox.Ok,
                   padrao=QMessageBox.NoButton, detalhe=None):
    """Caixa de mensagem no tema escuro, sem icones e com botoes em portugues."""
    caixa = QMessageBox(pai)
    caixa.setIcon(QMessageBox.NoIcon)
    caixa.setWindowTitle(titulo)
    caixa.setText(texto)
    if detalhe:
        caixa.setInformativeText(detalhe)
    caixa.setStandardButtons(botoes)
    if padrao != QMessageBox.NoButton:
        caixa.setDefaultButton(padrao)
    rotulos = (
        (QMessageBox.Yes, "Sim"),
        (QMessageBox.No, "Não"),
        (QMessageBox.Ok, "OK"),
        (QMessageBox.Cancel, "Cancelar"),
    )
    for botao, rotulo in rotulos:
        item = caixa.button(botao)
        if item is not None:
            item.setText(rotulo)
            item.setCursor(Qt.PointingHandCursor)
    resultado = caixa.exec()
    try:
        return QMessageBox.StandardButton(resultado)
    except Exception:
        return resultado


def pedir_texto(pai, titulo, rotulo):
    """Dialogo de texto no tema escuro. Devolve (texto, confirmado)."""
    dialogo = QInputDialog(pai)
    dialogo.setInputMode(QInputDialog.TextInput)
    dialogo.setWindowTitle(titulo)
    dialogo.setLabelText(rotulo)
    dialogo.setOkButtonText("Confirmar")
    dialogo.setCancelButtonText("Cancelar")
    dialogo.setMinimumWidth(440)
    confirmado = bool(dialogo.exec())
    return dialogo.textValue(), confirmado

def formatar_moeda(v7):
    if v7 is None:
        return "R$ --"
    return f"R$ {v7:.2f}".replace(".", ",")
def slug(v8):
    """'Sonho de Valsa' -> 'sonho_de_valsa' (para nome de arquivo)."""
    v8 = v8.lower()
    v9 = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "õ": "o", "ô": "o",
        "ú": "u",
        "ç": "c",
    }
    for v20, v21 in v9.items():
        v8 = v8.replace(v20, v21)
    v8 = v8.replace("(", "").replace(")", "")
    return "_".join(v8.split())
def imagem_existe(v10):
    if not v10:
        return False
    return (v2 / Path(v10).name).exists()
v6 = v1 / "comandas_pendentes.json"
def carregar_comandas_pendentes():
    """Lê o arquivo e devolve a lista já ordenada por chegada."""
    if not v6.exists():
        return []
    try:
        v22 = json.loads(v6.read_text(encoding="utf-8"))
        if not isinstance(v22, list):
            return []
        v22.sort(key=lambda v23: v23.get("timestamp", 0))
        return v22
    except Exception:
        return []
def salvar_lista_comandas(v11):
    v6.write_text(
        json.dumps(v11, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
def salvar_comanda_pendente(v12):
    v11 = carregar_comandas_pendentes()
    v11.append(v12)
    salvar_lista_comandas(v11)
def remover_comanda_pendente(v13):
    v11 = carregar_comandas_pendentes()
    v11 = [v23 for v23 in v11 if v23.get("id") != v13]
    salvar_lista_comandas(v11)
def comanda_tem_imediato(v12):
    return any(v54.get("imediato") for v54 in v12.get("itens", []))
class CardProduto(QFrame):
    """Card que se expande ao clique.
    Se o produto tiver `sabores`, ao clicar mostra a descrição + uma coluna
    com cada sabor (miniatura, nome e preço). Clicar em um sabor adiciona ao
    carrinho como "<produto> - <sabor>".
    """
    def __init__(self, v24, v25):
        super().__init__()
        self.produto = v24
        self.adicionar_callback = v25
        self.aberto = False
        self.sabores = v24.get("sabores") or []
        self.tem_sabores = len(self.sabores) > 0
        self.setObjectName("card")
        self.setMinimumHeight(385)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setCursor(Qt.PointingHandCursor)
        v26 = QVBoxLayout(self)
        v26.setContentsMargins(12, 12, 12, 14)
        v26.setSpacing(10)
        self.imagem = QLabel()
        self.imagem.setMinimumHeight(245)
        self.imagem.setMaximumHeight(245)
        self.imagem.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.imagem.setAlignment(Qt.AlignCenter)
        self.imagem.setStyleSheet(f"""
            QLabel {{
                background: {COR_IMAGEM_FUNDO};
                border-radius: 12px;
                color: {COR_IMAGEM_TEXTO};
                font-size: 13px;
            }}
        """)
        self.carregar_imagem()
        v26.addWidget(self.imagem)
        self.nome = QLabel(v24["nome"])
        self.nome.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.nome.setWordWrap(True)
        self.nome.setFixedHeight(44)
        self.nome.setStyleSheet(f"""
            QLabel {{
                color: {COR_TEXTO};
                font-size: 15px;
                font-weight: 600;
                background: transparent;
            }}
        """)
        v26.addWidget(self.nome)
        self.dica = QLabel(
            "Toque para escolher o sabor" if self.tem_sabores
            else "Toque para ver detalhes e preço"
        )
        self.dica.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.dica.setStyleSheet(f"""
            QLabel {{
                color: {COR_TEXTO_FRACO};
                font-size: 12px;
                background: transparent;
            }}
        """)
        v26.addWidget(self.dica)
        self.detalhes = QFrame()
        v27 = QHBoxLayout(self.detalhes)
        v27.setContentsMargins(0, 0, 0, 0)
        self.preco = QLabel(self.formatar_preco())
        self.preco.setStyleSheet(f"""
            QLabel {{
                color: {COR_VERDE_CLARO};
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        self.botao_adicionar = QPushButton("+")
        self.botao_adicionar.setFixedSize(42, 42)
        self.botao_adicionar.setCursor(Qt.PointingHandCursor)
        self.botao_adicionar.clicked.connect(self.adicionar)
        self.botao_adicionar.setStyleSheet(f"""
            QPushButton {{
                background: {COR_VERDE};
                color: {COR_SOBRE_VERDE};
                border: none;
                border-radius: 11px;
                font-size: 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: {COR_VERDE_CLARO}; }}
            QPushButton:pressed {{ background: {COR_VERDE_PRESS}; }}
        """)
        v27.addWidget(self.preco)
        v27.addStretch()
        v27.addWidget(self.botao_adicionar)
        self.descricao = QLabel(v24["descricao"])
        self.descricao.setWordWrap(True)
        self.descricao.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.descricao.setStyleSheet(f"""
            QLabel {{
                color: {COR_TEXTO_SUAVE};
                font-size: 12px;
                background: transparent;
            }}
        """)
        self.painel_sabores = QWidget()
        self.painel_sabores.setVisible(False)
        v28 = QVBoxLayout(self.painel_sabores)
        v28.setContentsMargins(0, 4, 0, 0)
        v28.setSpacing(6)
        v29 = QLabel("ESCOLHA O SABOR")
        v29.setStyleSheet(f"""
            QLabel {{
                color: {COR_VERDE};
                font-size: 11px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        espacar_letras(v29, 1.2)
        v28.addWidget(v29)
        for v30 in self.sabores:
            v28.addWidget(self.criar_linha_sabor(v30))
        self.detalhes.setVisible(False)
        self.descricao.setVisible(False)
        v26.addWidget(self.detalhes)
        v26.addWidget(self.descricao)
        v26.addWidget(self.painel_sabores)
        self.setStyleSheet(f"""
            QFrame#card {{
                background: {COR_SUPERFICIE};
                border: 1px solid {COR_BORDA};
                border-radius: 16px;
            }}
            QFrame#card:hover {{
                background: {COR_SUPERFICIE_2};
                border: 1px solid {COR_VERDE};
            }}
        """)
    def criar_linha_sabor(self, v30):
        v31 = QFrame()
        v31.setObjectName("sabor_linha")
        v31.setCursor(Qt.PointingHandCursor)
        v31.setStyleSheet(f"""
            QFrame#sabor_linha {{
                background: {COR_SUPERFICIE_2};
                border: 1px solid {COR_BORDA};
                border-radius: 10px;
            }}
            QFrame#sabor_linha:hover {{
                background: {COR_VERDE_TINT};
                border: 1px solid {COR_VERDE};
            }}
        """)
        v32 = QHBoxLayout(v31)
        v32.setContentsMargins(8, 6, 12, 6)
        v32.setSpacing(10)
        v33 = QLabel()
        v33.setFixedSize(52, 52)
        v33.setAlignment(Qt.AlignCenter)
        v33.setStyleSheet(f"""
            QLabel {{
                background: {COR_IMAGEM_FUNDO};
                border-radius: 8px;
                color: {COR_IMAGEM_TEXTO};
                font-size: 10px;
            }}
        """)
        v33.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        v34 = self.pixmap_do_sabor(v30)
        if not v34.isNull():
            v33.setPixmap(
                v34.scaled(
                    48, 48,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            v33.setText("Sem foto")
        v32.addWidget(v33)
        v10 = QLabel(v30["nome"])
        v10.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        v10.setStyleSheet(f"""
            QLabel {{
                color: {COR_TEXTO};
                font-size: 13px;
                font-weight: 600;
                background: transparent;
            }}
        """)
        v32.addWidget(v10)
        v32.addStretch()
        v35 = v30.get("preco", self.produto.get("preco"))
        v36 = QLabel(formatar_moeda(v35))
        v36.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        v36.setStyleSheet(f"""
            QLabel {{
                color: {COR_VERDE_CLARO};
                font-size: 13px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        v32.addWidget(v36)
        def _click(v42, v124=v30):
            if v42.button() == Qt.LeftButton:
                self.adicionar_sabor(v124)
        v31.mousePressEvent = _click
        return v31
    def pixmap_do_sabor(self, v30):
        """Tenta carregar a imagem do sabor.
        1) Se o sabor tem 'imagem' explícita, tenta essa.
        2) Senão, tenta '<base_produto>_<slug_sabor>.jpg'.
        3) Senão, tenta '<base_produto>_<slug_sabor>.png'.
        4) Senão, devolve QPixmap() vazio.
        """
        v37 = []
        if v30.get("imagem"):
            v37.append(v2 / Path(v30["imagem"]).name)
        v38 = slug(Path(self.produto["imagem"]).stem)
        v37.append(v2 / f"{v38}_{slug(v30['nome'])}.jpg")
        v37.append(v2 / f"{v38}_{slug(v30['nome'])}.png")
        for v39 in v37:
            v34 = QPixmap(str(v39))
            if not v34.isNull():
                return v34
        return QPixmap()
    def caminho_imagem(self):
        return v2 / Path(self.produto["imagem"]).name
    def carregar_imagem(self):
        v39 = self.caminho_imagem()
        v34 = QPixmap(str(v39))
        if v34.isNull():
            self.imagem.setText("Imagem não encontrada")
            return
        self._pixmap_original = v34
        self.atualizar_imagem()
    def atualizar_imagem(self):
        v34 = getattr(self, "_pixmap_original", QPixmap())
        if v34.isNull():
            return
        v40 = max(120, self.imagem.width() - 4)
        v41 = max(180, self.imagem.height() - 4)
        self.imagem.setPixmap(
            v34.scaled(
                v40,
                v41,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
    def resizeEvent(self, v42):
        self.atualizar_imagem()
        super().resizeEvent(v42)
    def formatar_preco(self):
        return formatar_moeda(self.produto.get("preco"))
    def mousePressEvent(self, v42):
        if v42.button() == Qt.LeftButton:
            if self.botao_adicionar.isVisible() and \
                    self.botao_adicionar.geometry().contains(v42.pos()):
                super().mousePressEvent(v42)
                return
            self.abrir_detalhes()
        super().mousePressEvent(v42)
    def abrir_detalhes(self):
        self.aberto = not self.aberto
        self.dica.setVisible(not self.aberto)
        if self.tem_sabores:
            self.detalhes.setVisible(False)
            self.descricao.setVisible(self.aberto)
            self.painel_sabores.setVisible(self.aberto)
        else:
            self.detalhes.setVisible(self.aberto)
            self.descricao.setVisible(self.aberto)
            self.painel_sabores.setVisible(False)
    def adicionar(self):
        if self.tem_sabores:
            self.aberto = True
            self.dica.setVisible(False)
            self.descricao.setVisible(True)
            self.painel_sabores.setVisible(True)
            return
        if self.produto.get("preco") is None:
            caixa_mensagem(
                self,
                "Produto",
                "Este produto ainda não possui preço cadastrado."
            )
            return
        self.adicionar_callback(self.produto)
    def adicionar_sabor(self, v30):
        v36 = v30.get("preco", self.produto.get("preco"))
        if v36 is None:
            caixa_mensagem(
                self,
                "Produto",
                "Este sabor ainda não possui preço cadastrado."
            )
            return
        v43 = dict(self.produto)
        v43["nome"] = f"{self.produto['nome']} - {v30['nome']}"
        v43["preco"] = v36
        v43["sabor"] = v30["nome"]
        v43.pop("sabores", None)
        v44 = Path(self.produto["imagem"]).stem
        v45 = slug(v44)
        v46 = f"{v45}_{slug(v30['nome'])}.jpg"
        if v30.get("imagem") and imagem_existe(v30["imagem"]):
            v43["imagem"] = v30["imagem"]
        elif imagem_existe(v46):
            v43["imagem"] = v46
        self.adicionar_callback(v43)
class CardComanda(QFrame):
    """Card que representa uma comanda no painel do administrador."""
    def __init__(self, v12, v47):
        super().__init__()
        self.comanda = v12
        self.marcar_pronto_callback = v47
        self.setObjectName("card_comanda")
        self.setFixedWidth(290)
        self.setMinimumHeight(230)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        v48 = comanda_tem_imediato(v12)
        v49 = COR_VERDE if v48 else COR_BORDA_FORTE
        self.setStyleSheet(f"""
            QFrame#card_comanda {{
                background: {COR_SUPERFICIE_2};
                border: 1px solid {v49};
                border-radius: 14px;
            }}
        """)
        v26 = QVBoxLayout(self)
        v26.setContentsMargins(16, 14, 16, 14)
        v26.setSpacing(9)
        v50 = QHBoxLayout()
        v50.setSpacing(8)
        v51 = QLabel(f"#{v12['numero']:04d}")
        v51.setStyleSheet(
            f"font-size: 18px; font-weight: bold; color: {COR_VERDE_CLARO}; "
            "background: transparent; border: none;"
        )
        v50.addWidget(v51)
        if v48:
            v127 = QLabel("IMEDIATO")
            v127.setStyleSheet(f"""
                QLabel {{
                    background: {COR_VERDE_TINT};
                    border: 1px solid {COR_VERDE_ESCURO};
                    border-radius: 9px;
                    padding: 2px 8px;
                    font-size: 10px;
                    font-weight: bold;
                    color: {COR_VERDE_CLARO};
                }}
            """)
            v50.addWidget(v127)
        v50.addStretch()
        try:
            v125 = datetime.fromisoformat(
                v12["criada_em"]
            ).strftime("%H:%M:%S")
        except Exception:
            v125 = "--:--"
        v52 = QLabel(v125)
        v52.setStyleSheet(
            f"font-size: 12px; color: {COR_TEXTO_FRACO}; "
            "background: transparent; border: none;"
        )
        v50.addWidget(v52)
        v26.addLayout(v50)
        v10 = QLabel(v12["nome"])
        v10.setWordWrap(True)
        v10.setStyleSheet(
            f"font-size: 15px; font-weight: bold; color: {COR_TEXTO}; "
            "background: transparent; border: none;"
        )
        v26.addWidget(v10)
        v53 = QFrame()
        v53.setFrameShape(QFrame.HLine)
        v53.setStyleSheet(
            f"background: {COR_BORDA_FORTE}; max-height: 1px; border: none;"
        )
        v26.addWidget(v53)
        for v54 in v12["itens"]:
            v31 = QLabel(f"{v54['quantidade']}×  {v54['nome']}")
            v31.setWordWrap(True)
            if v54.get("imediato"):
                v31.setStyleSheet(
                    f"font-size: 13px; color: {COR_VERDE_CLARO}; font-weight: bold; "
                    "background: transparent; border: none;"
                )
            else:
                v31.setStyleSheet(
                    f"font-size: 13px; color: {COR_TEXTO_SUAVE}; "
                    "background: transparent; border: none;"
                )
            v26.addWidget(v31)
        v26.addStretch()
        if "total" in v12:
            v128 = QHBoxLayout()
            v129 = QLabel("Total")
            v129.setStyleSheet(
                f"font-size: 12px; color: {COR_TEXTO_FRACO}; "
                "background: transparent; border: none;"
            )
            v128.addWidget(v129)
            v128.addStretch()
            v126 = QLabel(formatar_moeda(v12["total"]))
            v126.setStyleSheet(
                f"font-size: 14px; font-weight: bold; color: {COR_TEXTO}; "
                "background: transparent; border: none;"
            )
            v128.addWidget(v126)
            v26.addLayout(v128)
        v55 = QPushButton("Pronto")
        v55.setFixedHeight(38)
        v55.setCursor(Qt.PointingHandCursor)
        v55.clicked.connect(
            lambda: self.marcar_pronto_callback(self.comanda["id"])
        )
        v55.setStyleSheet(estilo_btn_primario(13, 9))
        v26.addWidget(v55)
class PaginaCarrinho(QWidget):
    """Página separada para visualizar, aumentar, diminuir e excluir produtos."""
    def __init__(self, v56, v57,
                 v58=None):
        super().__init__()
        self.voltar_callback = v56
        self.finalizar_callback = v57
        self.excluir_callback = v58
        self.itens = []
        v26 = QVBoxLayout(self)
        v26.setContentsMargins(40, 28, 40, 28)
        v26.setSpacing(18)
        v50 = QHBoxLayout()
        v50.setSpacing(18)
        v59 = QPushButton("Voltar")
        v59.setFixedSize(110, 44)
        v59.setCursor(Qt.PointingHandCursor)
        v59.clicked.connect(self.voltar_callback)
        v59.setStyleSheet(estilo_btn_secundario(14, 10))
        v50.addWidget(v59)
        v60 = QLabel("Seu pedido")
        v60.setStyleSheet(f"""
            font-size: 30px;
            font-weight: bold;
            color: {COR_TEXTO};
        """)
        v50.addWidget(v60)
        v50.addStretch()
        v26.addLayout(v50)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.conteudo = QWidget()
        self.lista_layout = QVBoxLayout(self.conteudo)
        self.lista_layout.setAlignment(Qt.AlignTop)
        self.lista_layout.setSpacing(10)
        self.scroll.setWidget(self.conteudo)
        v26.addWidget(self.scroll)
        v61 = QFrame()
        v61.setObjectName("rodape_carrinho")
        v61.setStyleSheet(f"""
            QFrame#rodape_carrinho {{
                background: {COR_SUPERFICIE};
                border: 1px solid {COR_BORDA};
                border-radius: 16px;
            }}
        """)
        v63 = QHBoxLayout(v61)
        v63.setContentsMargins(26, 16, 16, 16)
        v63.setSpacing(16)
        v64 = QVBoxLayout()
        v64.setSpacing(0)
        v65 = QLabel("TOTAL DO PEDIDO")
        v65.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {COR_TEXTO_FRACO}; "
            "background: transparent;"
        )
        espacar_letras(v65, 1.2)
        v64.addWidget(v65)
        self.total_label = QLabel("R$ 0,00")
        self.total_label.setStyleSheet(f"""
            font-size: 30px;
            font-weight: bold;
            color: {COR_VERDE_CLARO};
            background: transparent;
        """)
        v64.addWidget(self.total_label)
        v63.addLayout(v64)
        v63.addStretch()
        v62 = QPushButton("Conferir compra")
        v62.setFixedSize(230, 56)
        v62.setCursor(Qt.PointingHandCursor)
        v62.clicked.connect(self.finalizar_callback)
        v62.setStyleSheet(estilo_btn_primario(16, 12))
        v63.addWidget(v62)
        v26.addWidget(v61)
        self.atualizar()
    def definir_itens(self, v63):
        self.itens = v63
        self.atualizar()
    def atualizar(self):
        while self.lista_layout.count():
            v54 = self.lista_layout.takeAt(0)
            if v54.widget():
                v54.widget().deleteLater()
        if not self.itens:
            v118 = QLabel(
                "Seu carrinho está vazio."
                f"<br><span style='font-size: 14px; font-weight: normal; "
                f"color: {COR_TEXTO_FRACO};'>"
                "Volte ao cardápio e adicione produtos ao pedido.</span>"
            )
            v118.setAlignment(Qt.AlignCenter)
            v118.setStyleSheet(f"""
                font-size: 20px;
                font-weight: 600;
                color: {COR_TEXTO_SUAVE};
                padding: 80px;
            """)
            self.lista_layout.addWidget(v118)
            self.total_label.setText(formatar_moeda(0))
            return
        v64 = 0
        for v65, v54 in enumerate(self.itens):
            v24 = v54["produto"]
            v88 = v54["quantidade"]
            v127 = v24["preco"] * v88
            v64 += v127
            v31 = QFrame()
            v31.setObjectName("linha_item")
            v31.setStyleSheet(f"""
                QFrame#linha_item {{
                    background: {COR_SUPERFICIE};
                    border: 1px solid {COR_BORDA};
                    border-radius: 14px;
                }}
            """)
            v32 = QHBoxLayout(v31)
            v32.setContentsMargins(14, 12, 18, 12)
            v32.setSpacing(14)
            v128 = QLabel()
            v128.setFixedSize(88, 78)
            v128.setAlignment(Qt.AlignCenter)
            v128.setStyleSheet(f"""
                QLabel {{
                    background: {COR_IMAGEM_FUNDO};
                    border-radius: 10px;
                    color: {COR_IMAGEM_TEXTO};
                    font-size: 11px;
                }}
            """)
            v34 = QPixmap(str(v2 / Path(v24["imagem"]).name))
            if not v34.isNull():
                v128.setPixmap(
                    v34.scaled(
                        78, 68,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
            else:
                v128.setText("Sem foto")
            v32.addWidget(v128)
            v129 = QVBoxLayout()
            v129.setSpacing(3)
            v10 = QLabel(v24["nome"])
            v10.setStyleSheet(
                f"font-size: 16px; font-weight: bold; color: {COR_TEXTO};"
            )
            v129.addWidget(v10)
            v36 = QLabel(f"{formatar_moeda(v24['preco'])} cada")
            v36.setStyleSheet(f"font-size: 13px; color: {COR_TEXTO_SUAVE};")
            v129.addWidget(v36)
            v32.addLayout(v129)
            v32.addStretch()
            v66 = QFrame()
            v66.setObjectName("passo_qtd")
            v66.setStyleSheet(f"""
                QFrame#passo_qtd {{
                    background: {COR_SUPERFICIE_2};
                    border: 1px solid {COR_BORDA_FORTE};
                    border-radius: 11px;
                }}
            """)
            v67 = QHBoxLayout(v66)
            v67.setContentsMargins(4, 4, 4, 4)
            v67.setSpacing(2)
            v130 = QPushButton("−")
            v130.setFixedSize(36, 36)
            v130.setCursor(Qt.PointingHandCursor)
            v130.setStyleSheet(estilo_btn_passo())
            v130.clicked.connect(
                lambda v142, v135=v65: self.alterar_quantidade(v135, -1)
            )
            v131 = QLabel(str(v88))
            v131.setFixedWidth(34)
            v131.setAlignment(Qt.AlignCenter)
            v131.setStyleSheet(
                f"font-size: 16px; font-weight: bold; color: {COR_TEXTO};"
            )
            v132 = QPushButton("+")
            v132.setFixedSize(36, 36)
            v132.setCursor(Qt.PointingHandCursor)
            v132.setStyleSheet(estilo_btn_passo())
            v132.clicked.connect(
                lambda v142, v135=v65: self.alterar_quantidade(v135, 1)
            )
            v67.addWidget(v130)
            v67.addWidget(v131)
            v67.addWidget(v132)
            excluir = QPushButton("Excluir")
            excluir.setFixedHeight(40)
            excluir.setCursor(Qt.PointingHandCursor)
            excluir.setStyleSheet(estilo_btn_perigo(13, 10))
            excluir.clicked.connect(
                lambda v142, v135=v65: self.excluir(v135)
            )
            v133 = QLabel(formatar_moeda(v127))
            v133.setFixedWidth(110)
            v133.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            v133.setStyleSheet(
                f"font-size: 17px; font-weight: bold; color: {COR_VERDE_CLARO};"
            )
            v32.addWidget(v66)
            v32.addWidget(excluir)
            v32.addWidget(v133)
            self.lista_layout.addWidget(v31)
        self.total_label.setText(formatar_moeda(v64))
    def alterar_quantidade(self, v65, v66):
        self.itens[v65]["quantidade"] += v66
        if self.itens[v65]["quantidade"] <= 0:
            self.itens.pop(v65)
        self.atualizar()
        if self.excluir_callback:
            self.excluir_callback()
    def excluir(self, v65):
        v24 = self.itens[v65]["produto"]
        v68 = caixa_mensagem(
            self,
            "Excluir item",
            f"Tem certeza que deseja excluir <b>{v24['nome']}</b> "
            "do carrinho?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
            "Esta ação removerá o item do pedido."
        )
        if v68 == QMessageBox.Yes:
            self.itens.pop(v65)
            self.atualizar()
            if self.excluir_callback:
                self.excluir_callback()
    def obter_total(self):
        return sum(
            v54["produto"]["preco"] * v54["quantidade"]
            for v54 in self.itens
        )

ARQUIVO_PRODUTOS = v1 / "produtos.json"

def carregar_produtos(v):
    if ARQUIVO_PRODUTOS.exists():
        try:
            x = json.loads(ARQUIVO_PRODUTOS.read_text(encoding="utf-8"))
            if isinstance(x, dict):
                return x
        except Exception:
            pass
    ARQUIVO_PRODUTOS.write_text(
        json.dumps(v, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return v

def salvar_produtos(v):
    ARQUIVO_PRODUTOS.write_text(
        json.dumps(v, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

class Totem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cantina do Pablo")
        self.setObjectName("janela")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.resize(1280, 800)
        self.setMinimumSize(1000, 650)
        self.carrinho = []
        self.arquivo_contador = v1 / "contador_comandas.json"
        self.produtos = {'Cup Noodles': [{'nome': 'Cup Noodles Cheddar',
                              'descricao': 'Cup Noodles Cheddar para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_cheddar.png'},
                             {'nome': 'Cup Noodles Queijo',
                              'descricao': 'Bolonhesa',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_queijo.png'},
                             {'nome': 'Cup Noodles Seafood',
                              'descricao': 'Cup Noodles Seafood para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_seafood.png'},
                             {'nome': 'Cup Noodles Costela',
                              'descricao': 'Cup Noodles Costela para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_costela.png'},
                             {'nome': 'Cup Noodles Feijoada',
                              'descricao': 'Cup Noodles Feijoada para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_feijoada.png'},
                             {'nome': 'Cup Noodles Costela 2',
                              'descricao': 'Cup Noodles Costela 2 para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_costela_2.jpg'},
                             {'nome': 'Cup Noodles Carne',
                              'descricao': 'Cup Noodles Carne para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_carne.jpg'},
                             {'nome': 'Cup Noodles Teriyaki',
                              'descricao': 'Cup Noodles Teriyaki para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_teriyaki.png'},
                             {'nome': 'Cup Noodles Curry',
                              'descricao': 'Cup Noodles Curry para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_curry.png'},
                             {'nome': 'Cup Noodles Yakissoba',
                              'descricao': 'Cup Noodles Yakissoba para uma refeição prática e rápida.',
                              'preco': 8.0,
                              'imagem': 'cup_noodles_yakissoba.png'}],
             'Doces': [{'nome': 'Bolinho Chocolate Recheado',
                                     'descricao': 'Bolinho Chocolate Recheado para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'bolinho_chocolate_recheado.png'},
                                    {'nome': 'Trakinas Chocolate 126g',
                                     'descricao': 'Trakinas Chocolate 126g para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trakinas_chocolate_126g.jpg'},
                                    {'nome': 'Trakinas Chocolate',
                                     'descricao': 'Trakinas Chocolate para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trakinas_chocolate.jpg'},
                                    {'nome': 'Bolo Chocolate',
                                     'descricao': 'Bolo Chocolate para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'bolo_chocolate.png'},
                                    {'nome': 'Trento Branco',
                                     'descricao': 'Trento Branco para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_branco.png'},
                                    {'nome': 'Trento Morango',
                                     'descricao': 'Trento Morango para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_morango.jpg'},
                                    {'nome': 'Trento Chocolate 1',
                                     'descricao': 'Trento Chocolate 1 para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_chocolate_1.jpg'},
                                    {'nome': 'Trento Morango 2',
                                     'descricao': 'Trento Morango 2 para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_morango_2.png'},
                                    {'nome': 'Trento Chocolate 2',
                                     'descricao': 'Trento Chocolate 2 para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_chocolate_2.jpg'},
                                    {'nome': 'Nougat Amendoim',
                                     'descricao': 'Nougat Amendoim para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'nougat_amendoim.png'},
                                    {'nome': 'Trento Chocolate 3',
                                     'descricao': 'Trento Chocolate 3 para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_chocolate_3.png'},
                                    {'nome': 'Doce de Abóbora',
                                     'descricao': 'Doce de abóbora para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'biscoito_coracao.png'},
                                    {'nome': 'Ouro Branco',
                                     'descricao': 'Ouro Branco para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'ouro_branco.png'},
                                    {'nome': 'Suspiro Chocolate 1',
                                     'descricao': 'Suspiro Chocolate 1 para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'suspiro_chocolate_1.png'},
                                    {'nome': 'Sonho De Valsa',
                                     'descricao': 'Sonho De Valsa para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'sonho_de_valsa.png'},
                                    {'nome': 'Trento Branco 2',
                                     'descricao': 'Trento Branco 2 para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_branco_2.png'},
                                    {'nome': 'Trento Creme',
                                     'descricao': 'Trento Creme para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_creme.png'},
                                    {'nome': 'Trento Duo',
                                     'descricao': 'Trento Duo para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_duo.png'},
                                    {'nome': 'Trento Leite',
                                     'descricao': 'Trento Leite para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_leite.png'},
                                    {'nome': 'Trento Limao',
                                     'descricao': 'Trento Limao para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_limao.png'},
                                    {'nome': 'Trento Trufa Chocolate',
                                     'descricao': 'Trento Trufa Chocolate para matar a vontade de um doce.',
                                     'preco': 4.5,
                                     'imagem': 'trento_trufa_chocolate.png'},
                                    {'nome': 'Doce De Leite',
                                     'descricao': 'Doce De Leite para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'doce_de_leite.png'},
                                    {'nome': 'Doce De Copo Banana',
                                     'descricao': 'Doce De Copo Banana para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'doce_de_copo_banana.png'},
                                    {'nome': 'Doce De Mocoto',
                                     'descricao': 'Doce De Mocoto para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'doce_de_mocoto.png'},
                                    {'nome': 'Maria Mole',
                                     'descricao': 'Maria Mole para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'maria_mole.png'},
                                    {'nome': 'Paçoca Rolha',
                                     'descricao': 'Paçoca Rolha para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'pacoca_rolha.png'},
                                    {'nome': 'Pacoquita',
                                     'descricao': 'Pacoquita para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'pacoquita.png'},
                                    {'nome': 'Pe De Moleque',
                                     'descricao': 'Pe De Moleque para um lanche doce e descontraído.',
                                     'preco': 4.0,
                                     'imagem': 'pe_de_moleque.png'},
                                    {'nome': 'Pe De Moleque 2',
                                     'descricao': 'Pé de moça',
                                     'preco': 4.0,
                                     'imagem': 'pe_de_moleque_2.png'},
                                    {'nome': 'Bala De Gelatina Morango',
                                     'descricao': 'Doce de geleia da água',
                                     'preco': 2.5,
                                     'imagem': 'bala_de_gelatina_morango.png'}],
             'Doces e Pipocas': [{'nome': 'Pipoca Bacon',
                                  'descricao': 'Pipoca Bacon para um lanche doce e descontraído.',
                                  'preco': 4.0,
                                  'imagem': 'pipoca_bacon.png'},
                                 {'nome': 'Pipoca Cinema',
                                  'descricao': 'Pipoca Cinema para um lanche doce e descontraído.',
                                  'preco': 4.0,
                                  'imagem': 'pipoca_cinema.png'},
                                 {'nome': 'Pipoca Manteiga',
                                  'descricao': 'Pipoca Manteiga para um lanche doce e descontraído.',
                                  'preco': 4.0,
                                  'imagem': 'pipoca_manteiga.png'},
                                 {'nome': 'Pipoca Natural',
                                  'descricao': 'Pipoca Natural para um lanche doce e descontraído.',
                                  'preco': 4.0,
                                  'imagem': 'pipoca_natural.png'},
                                 {'nome': 'Pipoca Pizza',
                                  'descricao': 'Pipoca Pizza para um lanche doce e descontraído.',
                                  'preco': 4.0,
                                  'imagem': 'pipoca_pizza.png'},
                                 {'nome': 'Pipoca Queijo',
                                  'descricao': 'Pipoca Queijo para um lanche doce e descontraído.',
                                  'preco': 4.0,
                                  'imagem': 'pipoca_queijo.png'}],
             'Refeições': [{'nome': 'Bife Acebolado',
                            'descricao': 'Bife acebolado servido como opção de refeição da cantina.',
                            'preco': 20.0,
                            'imagem': 'bife_acebolado.jpg',
                            'imediato': True},
                           {'nome': 'Caldo',
                            'descricao': 'Caldo tradicional para aquecer o intervalo.',
                            'preco': 8.0,
                            'imagem': 'caldo.jpg',
                            'imediato': True},
                           {'nome': 'Caldo de Abóbora',
                            'descricao': 'Caldo cremoso de abóbora para o intervalo.',
                            'preco': 8.0,
                            'imagem': 'caldo_abobora.jpg',
                            'imediato': True},
                           {'nome': 'Caldo de Feijão',
                            'descricao': 'Caldo saboroso de feijão para o intervalo.',
                            'preco': 8.0,
                            'imagem': 'caldo_feijao.jpg',
                            'imediato': True},
                           {'nome': 'Caldo de Mandioca',
                            'descricao': 'Caldo cremoso de mandioca para o intervalo.',
                            'preco': 8.0,
                            'imagem': 'caldo_mandioca.jpg',
                            'imediato': True},
                           {'nome': 'Caldo Verde',
                            'descricao': 'Caldo verde preparado para uma refeição quente e prática.',
                            'preco': 8.0,
                            'imagem': 'caldo_verde.jpg',
                            'imediato': True},
                           {'nome': 'Carne Cozida',
                            'descricao': 'Carne cozida como opção de refeição da cantina.',
                            'preco': 20.0,
                            'imagem': 'carne_cozida.jpg',
                            'imediato': True},
                           {'nome': 'Churrasco',
                            'descricao': 'Churrasco preparado para uma refeição completa.',
                            'preco': 20.0,
                            'imagem': 'churrasco.jpg',
                            'imediato': True},
                           {'nome': 'Espeto',
                            'descricao': 'Espeto preparado na cantina para um lanche reforçado.',
                            'preco': 9.0,
                            'imagem': 'espeto.jpg',
                            'imediato': True},
                           {'nome': 'Espeto de Carne',
                            'descricao': 'Espeto de carne preparado para o intervalo.',
                            'preco': 9.0,
                            'imagem': 'espeto_carne.jpg',
                            'imediato': True},
                           {'nome': 'Espeto de Coração',
                            'descricao': 'Espeto de coração preparado para o intervalo.',
                            'preco': 9.0,
                            'imagem': 'espeto_coracao.jpg',
                            'imediato': True},
                           {'nome': 'Espeto de Medalhão',
                            'descricao': 'Espeto de medalhão preparado para o intervalo.',
                            'preco': 9.0,
                            'imagem': 'espeto_medalhao.jpg',
                            'imediato': True},
                           {'nome': 'Frango Empanado com Fritas',
                            'descricao': 'Frango empanado com fritas como opção de refeição.',
                            'preco': 20.0,
                            'imagem': 'frango_empanado.jpg',
                            'imediato': True},
                           {'nome': 'Frango Grelhado',
                            'descricao': 'Frango grelhado como opção de refeição da cantina.',
                            'preco': 20.0,
                            'imagem': 'frango_grelhado.jpg',
                            'imediato': True},
                           {'nome': 'Strogonoff de Carne',
                            'descricao': 'Strogonoff de carne como opção de refeição da cantina.',
                            'preco': 20.0,
                            'imagem': 'strogonoff_carne.jpg',
                            'imediato': True},
                           {'nome': 'Strogonoff de Frango',
                            'descricao': 'Strogonoff de frango como opção de refeição da cantina.',
                            'preco': 20.0,
                            'imagem': 'strogonoff_frango.jpg',
                            'imediato': True}],
             'Bebidas': [{'nome': 'Monster Ultra',
                          'descricao': 'Monster Ultra gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_ultra.png'},
                         {'nome': 'Monster Energy',
                          'descricao': 'Monster Energy gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_energy.png'},
                         {'nome': 'Agua Mineral 500ml 1',
                          'descricao': 'Agua Mineral 500ml 1 gelado para acompanhar seu pedido com '
                                       'praticidade.',
                          'preco': 3.5,
                          'imagem': 'agua_mineral_500ml_1.png'},
                         {'nome': 'Coca Cola Lata',
                          'descricao': 'Coca Cola Lata gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'coca_cola_lata.png'},
                         {'nome': 'Monster Dragon Ice Tea Lemon',
                          'descricao': 'Monster Dragon Ice Tea Lemon gelado para acompanhar seu pedido com '
                                       'praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_dragon_ice_tea_lemon.png'},
                         {'nome': 'Guarana Antarctica Zero',
                          'descricao': 'Guarana Antarctica Zero gelado para acompanhar seu pedido com '
                                       'praticidade.',
                          'preco': 5.0,
                          'imagem': 'guarana_antarctica_zero.jpg'},
                         {'nome': 'Monster Juice 1',
                          'descricao': 'Monster Juice 1 gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_juice_1.jpg'},
                         {'nome': 'Monster Juice 2',
                          'descricao': 'Monster Juice 2 gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_juice_2.jpg'},
                         {'nome': 'Fanta Laranja',
                          'descricao': 'Fanta Laranja gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'fanta_laranja.jpg'},
                         {'nome': 'Monster Juice 3',
                          'descricao': 'Monster Juice 3 gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_juice_3.png'},
                         {'nome': 'Monster Energy Roxo',
                          'descricao': 'Monster Energy Roxo gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_energy_roxo.png'},
                         {'nome': 'Monster Energy Zero',
                          'descricao': 'Monster Energy Zero gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_energy_zero.png'},
                         {'nome': 'Monster Energy Ultra Azul',
                          'descricao': 'Monster Energy Ultra Azul gelado para acompanhar seu pedido com '
                                       'praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_energy_ultra_azul.png'},
                         {'nome': 'Monster Juice Mango',
                          'descricao': 'Monster Juice Mango gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_juice_mango.png'},
                         {'nome': 'Monster Juice Verde',
                          'descricao': 'Monster Juice Verde gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_juice_verde.png'},
                         {'nome': 'Monster Energy Aqua',
                          'descricao': 'Monster Energy Aqua gelado para acompanhar seu pedido com praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_energy_aqua.png'},
                         {'nome': 'Monster Energy Ultra Rosa',
                          'descricao': 'Monster Energy Ultra Rosa gelado para acompanhar seu pedido com '
                                       'praticidade.',
                          'preco': 6.0,
                          'imagem': 'monster_energy_ultra_rosa.png'},
                         {'nome': 'Coca Cola Zero Lata',
                          'descricao': 'Coca Cola Zero Lata gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'coca_cola_zero_lata.png'},
                         {'nome': 'Fanta Uva',
                          'descricao': 'Fanta Uva gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'fanta_uva.png'},
                         {'nome': 'Fanta Laranja 2',
                          'descricao': 'Fanta Laranja 2 gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'fanta_laranja_2.png'},
                         {'nome': 'Sprite Limao',
                          'descricao': 'Sprite Limao gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'sprite_limao.png'},
                         {'nome': 'Sukita Uva',
                          'descricao': 'Sukita Uva gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'sukita_uva.png'},
                         {'nome': 'Sukita Laranja',
                          'descricao': 'Sukita Laranja gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'sukita_laranja.png'},
                         {'nome': 'Coca Cola Pet',
                          'descricao': 'Coca Cola Pet gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'coca_cola_pet.png'},
                         {'nome': 'Coca Cola Zero Pet',
                          'descricao': 'Coca Cola Zero Pet gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'coca_cola_zero_pet.png'},
                         {'nome': 'Guarana Antarctica',
                          'descricao': 'Guarana Antarctica gelado para acompanhar seu pedido com praticidade.',
                          'preco': 5.0,
                          'imagem': 'guarana_antarctica.png'},
                         {'nome': 'Suco Natural Laranja',
                          'descricao': 'Suco Natural Laranja gelado para acompanhar seu pedido com '
                                       'praticidade.',
                          'preco': 5.0,
                          'imagem': 'suco_natural_laranja.png'}],
             'Salgados e Lanches': [{'nome': 'Sanduiche Misto',
                                     'descricao': 'Sanduiche Misto preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'sanduiche_misto.png'},
                                    {'nome': 'Pão De Queijo',
                                     'descricao': 'Pão De Queijo preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'pao_de_queijo.jpg'},
                                    {'nome': 'Coxinha',
                                     'descricao': 'Coxinha preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'coxinha.png'},
                                    {'nome': 'Pão De Batata',
                                     'descricao': 'Pão De Batata preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'pao_de_batata.png'},
                                    {'nome': 'Enroladinho De Salsicha',
                                     'descricao': 'Enroladinho De Salsicha preparado para um lanche rápido '
                                                  'durante o intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'enroladinho_de_salsicha.png'},
                                    {'nome': 'Esfiha De Carne',
                                     'descricao': 'Esfiha De Carne preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'esfiha_de_carne.png'},
                                    {'nome': 'Croissant',
                                     'descricao': 'Croissant preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'croissant.jpg'},
                                    {'nome': 'Pão De Batata Calabresa',
                                     'descricao': 'Pão De Batata Calabresa preparado para um lanche rápido '
                                                  'durante o intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'pao_de_batata_calabresa.png'},
                                    {'nome': 'Pizza Enrolada',
                                     'descricao': 'Pizza Enrolada preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'pizza_enrolada.png'},
                                    {'nome': 'Risole',
                                     'descricao': 'Risole preparado para um lanche rápido durante o intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'risole.png'},
                                    {'nome': 'Kibe De Carne',
                                     'descricao': 'Kibe De Carne preparado para um lanche rápido durante o '
                                                  'intervalo.',
                                     'preco': 6.5,
                                     'imagem': 'kibe_de_carne.png'}],
             'Sorvetes': [{'nome': 'Sorvete Cremosinho Coco Banana',
                           'descricao': 'Sorvete Cremosinho Coco Banana cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_coco_banana.png'},
                          {'nome': 'Sorvete Cremosinho Coco',
                           'descricao': 'Sorvete Cremosinho Coco cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_coco.png'},
                          {'nome': 'Sorvete Cremosinho Frutas Tropicais',
                           'descricao': 'Sorvete Cremosinho Frutas Tropicais cremoso para refrescar o '
                                        'intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_frutas_tropicais.png'},
                          {'nome': 'Sorvete Cremosinho Babaloo',
                           'descricao': 'Sorvete Cremosinho Babaloo cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_babaloo.jpg'},
                          {'nome': 'Sorvete Cremosinho Kiwi',
                           'descricao': 'Sorvete Cremosinho Kiwi cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_kiwi.png'},
                          {'nome': 'Sorvete Cremosinho Leite Condensado',
                           'descricao': 'Sorvete Cremosinho Leite Condensado cremoso para refrescar o '
                                        'intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_leite_condensado.png'},
                          {'nome': 'Sorvete Cremosinho Manga',
                           'descricao': 'Sorvete Cremosinho Manga cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_manga.png'},
                          {'nome': 'Sorvete Cremosinho Maracuja',
                           'descricao': 'Sorvete Cremosinho Maracuja cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_maracuja.png'},
                          {'nome': 'Sorvete Cremosinho Morango 1',
                           'descricao': 'Sorvete Cremosinho Morango 1 cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_morango_1.png'},
                          {'nome': 'Sorvete Cremosinho Morango 2',
                           'descricao': 'Sorvete Cremosinho Morango 2 cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_morango_2.png'},
                          {'nome': 'Sorvete Cremosinho Uva',
                           'descricao': 'Sorvete Cremosinho Uva cremoso para refrescar o intervalo.',
                           'preco': 4.5,
                           'imagem': 'sorvete_cremosinho_uva.png'}],
             'Balas e Chicletes': [{'nome': 'Bala Yogurte Morango',
                                    'descricao': 'Bala Yogurte Morango para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'bala_yogurte_morango.jpg'},
                                   {'nome': 'Halls Cereja',
                                    'descricao': 'Halls Cereja para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_cereja.png'},
                                   {'nome': 'Halls Melancia',
                                    'descricao': 'Halls Melancia para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_melancia.png'},
                                   {'nome': 'Halls Menta',
                                    'descricao': 'Halls Menta para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_menta.png'},
                                   {'nome': 'Halls Menta Prata',
                                    'descricao': 'Halls Menta Prata para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_menta_prata.png'},
                                   {'nome': 'Halls Morango',
                                    'descricao': 'Halls Morango para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_morango.png'},
                                   {'nome': 'Halls Preto',
                                    'descricao': 'Halls Preto para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_preto.png'},
                                   {'nome': 'Halls Uva Verde',
                                    'descricao': 'Halls Uva Verde para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'halls_uva_verde.png'},
                                   {'nome': 'Trident Melancia',
                                    'descricao': 'Trident Melancia para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_melancia.jpg'},
                                   {'nome': 'Bubbaloo Azul',
                                    'descricao': 'Bubbaloo Azul para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'bubbaloo_azul.jpg'},
                                   {'nome': 'Bubbaloo Azul 2',
                                    'descricao': 'Bubbaloo Azul 2 para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'bubbaloo_azul_2.jpg'},
                                   {'nome': 'Bubbaloo Cereja',
                                    'descricao': 'Bubbaloo Cereja para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'bubbaloo_cereja.jpg'},
                                   {'nome': 'Bubbaloo Tutti Frutti',
                                    'descricao': 'Bubbaloo Tutti Frutti para um toque doce e refrescante no '
                                                 'seu intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'bubbaloo_tutti_frutti.jpg'},
                                   {'nome': 'Bubbaloo Cereja 2',
                                    'descricao': 'Bubbaloo Cereja 2 para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'bubbaloo_cereja_2.png'},
                                   {'nome': 'Trident Melancia 2',
                                    'descricao': 'Trident Melancia 2 para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_melancia_2.png'},
                                   {'nome': 'Trident Canela',
                                    'descricao': 'Trident Canela para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_canela.png'},
                                   {'nome': 'Trident Cereja',
                                    'descricao': 'Trident Cereja para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_cereja.png'},
                                   {'nome': 'Trident Fresh',
                                    'descricao': 'Trident Fresh para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_fresh.png'},
                                   {'nome': 'Trident Hortela',
                                    'descricao': 'Trident Hortela para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_hortela.png'},
                                   {'nome': 'Trident Menta',
                                    'descricao': 'Trident Menta para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_menta.png'},
                                   {'nome': 'Trident Tutti Frutti',
                                    'descricao': 'Trident Tutti Frutti para um toque doce e refrescante no seu '
                                                 'intervalo.',
                                    'preco': 2.5,
                                    'imagem': 'trident_tutti_frutti.png'}],
             'Outros': [{'nome': 'Canetas Bic',
                         'descricao': 'Canetas Bic disponível na Cantina do IFSP CJO.',
                         'preco': 5.0,
                         'imagem': 'canetas_bic.png'}]}
        self.stack = QStackedWidget()
        self.pagina_boas_vindas = self.criar_pagina_boas_vindas()
        self.pagina_menu = self.criar_pagina_menu()
        self.pagina_carrinho = PaginaCarrinho(
            self.voltar_para_menu,
            self.confirmar_compra,
            self.atualizar_previa_carrinho,
        )
        self.stack.addWidget(self.pagina_boas_vindas)
        self.stack.addWidget(self.pagina_menu)
        self.stack.addWidget(self.pagina_carrinho)
        v26 = QVBoxLayout(self)
        v26.setContentsMargins(0, 0, 0, 0)
        v26.addWidget(self.stack)
        self.mostrar_produtos("Doces")
        self.atualizar_previa_carrinho()
    def criar_pagina_boas_vindas(self):
        v69 = QWidget()
        v69.setObjectName("pagina_boas_vindas")
        v69.setAttribute(Qt.WA_StyledBackground, True)
        v69.setStyleSheet(f"""
            QWidget#pagina_boas_vindas {{
                background: qradialgradient(
                    cx: 0.5, cy: 0.40, radius: 0.85, fx: 0.5, fy: 0.40,
                    stop: 0 #10301f, stop: 0.55 #0a1510, stop: 1 {COR_FUNDO}
                );
            }}
        """)
        v26 = QVBoxLayout(v69)
        v26.setAlignment(Qt.AlignCenter)
        v26.setSpacing(0)
        v70 = QLabel("P")
        v70.setFixedSize(96, 96)
        v70.setAlignment(Qt.AlignCenter)
        v70.setStyleSheet(estilo_marca(48, 26))
        v26.addWidget(v70, alignment=Qt.AlignCenter)
        v26.addSpacing(30)
        v73 = QLabel("AUTOATENDIMENTO")
        v73.setAlignment(Qt.AlignCenter)
        v73.setStyleSheet(
            f"font-size: 13px; font-weight: bold; color: {COR_VERDE}; "
            "background: transparent;"
        )
        espacar_letras(v73, 3)
        v26.addWidget(v73)
        v26.addSpacing(12)
        v60 = QLabel(
            f"Cantina do <span style='color: {COR_VERDE};'>Pablo</span>"
        )
        v60.setAlignment(Qt.AlignCenter)
        v60.setStyleSheet(f"""
            font-size: 58px;
            font-weight: bold;
            color: {COR_TEXTO};
            background: transparent;
        """)
        v26.addWidget(v60)
        v26.addSpacing(14)
        v71 = QLabel("Bem vindo")
        v71.setAlignment(Qt.AlignCenter)
        v71.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 600;
            color: {COR_TEXTO};
            background: transparent;
        """)
        v26.addWidget(v71)
        v26.addSpacing(6)
        v74 = QLabel("Escolha seus produtos e finalize o pedido em poucos passos.")
        v74.setAlignment(Qt.AlignCenter)
        v74.setStyleSheet(
            f"font-size: 16px; color: {COR_TEXTO_SUAVE}; background: transparent;"
        )
        v26.addWidget(v74)
        v26.addSpacing(42)
        v72 = QPushButton("Começar pedido")
        v72.setFixedSize(300, 64)
        v72.setCursor(Qt.PointingHandCursor)
        v72.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.pagina_menu)
        )
        v72.setStyleSheet(estilo_btn_primario(18, 14))
        v26.addWidget(v72, alignment=Qt.AlignCenter)
        return v69
    def criar_pagina_menu(self):
        v69 = QWidget()
        v73 = QHBoxLayout(v69)
        v73.setContentsMargins(0, 0, 0, 0)
        v73.setSpacing(0)
        v74 = QFrame()
        v74.setObjectName("sidebar")
        v74.setFixedWidth(210)
        v74.setStyleSheet(f"""
            QFrame#sidebar {{
                background: {COR_SUPERFICIE};
                border-right: 1px solid {COR_BORDA};
            }}
        """)
        v75 = QVBoxLayout(v74)
        v75.setContentsMargins(14, 20, 14, 16)
        v75.setSpacing(6)
        v50 = QHBoxLayout()
        v50.setSpacing(10)
        v70 = QLabel("P")
        v70.setFixedSize(40, 40)
        v70.setAlignment(Qt.AlignCenter)
        v70.setStyleSheet(estilo_marca(20, 11))
        v50.addWidget(v70)
        v83 = QVBoxLayout()
        v83.setSpacing(0)
        v84 = QLabel("Cantina")
        v84.setStyleSheet(
            f"font-size: 15px; font-weight: bold; color: {COR_TEXTO}; "
            "background: transparent;"
        )
        v85 = QLabel("do Pablo")
        v85.setStyleSheet(
            f"font-size: 12px; font-weight: 600; color: {COR_VERDE}; "
            "background: transparent;"
        )
        v83.addWidget(v84)
        v83.addWidget(v85)
        v50.addLayout(v83)
        v50.addStretch()
        v75.addLayout(v50)
        v75.addSpacing(22)
        v86 = QLabel("CATEGORIAS")
        v86.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: {COR_TEXTO_FRACO}; "
            "background: transparent; padding-left: 4px;"
        )
        espacar_letras(v86, 1.5)
        v75.addWidget(v86)
        v75.addSpacing(2)
        self.botoes_categoria = {}
        v76 = [
            ("Doces", "Doces"),
            ("Refeições", "Refeições"),
            ("Salgados", "Salgados e Lanches"),
            ("Pipocas", "Doces e Pipocas"),
            ("Bebidas", "Bebidas"),
            ("Cup Noodles", "Cup Noodles"),
            ("Sorvetes", "Sorvetes"),
            ("Balas", "Balas e Chicletes"),
            ("Outros", "Outros"),
        ]
        for v8, v81 in v76:
            self.criar_botao_categoria(v75, v8, v81)
        v75.addStretch()
        self.previa_carrinho = QLabel(self.formatar_previa(0, 0))
        self.previa_carrinho.setTextFormat(Qt.RichText)
        self.previa_carrinho.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.previa_carrinho.setStyleSheet(f"""
            QLabel {{
                background: {COR_SUPERFICIE_2};
                border: 1px solid {COR_BORDA};
                border-radius: 12px;
                padding: 12px 14px;
            }}
        """)
        v75.addWidget(self.previa_carrinho)
        v77 = QPushButton("Carrinho")
        v77.setFixedHeight(50)
        v77.setCursor(Qt.PointingHandCursor)
        v77.clicked.connect(self.abrir_carrinho)
        v77.setStyleSheet(estilo_btn_primario(15, 12))
        v75.addWidget(v77)
        v73.addWidget(v74)
        v78 = QFrame()
        v78.setObjectName("conteudo_menu")
        v78.setStyleSheet("QFrame#conteudo_menu { background: transparent; }")
        v79 = QVBoxLayout(v78)
        v79.setContentsMargins(28, 24, 28, 16)
        v79.setSpacing(14)
        v50 = QHBoxLayout()
        self.titulo = QLabel("Refeições")
        self.titulo.setStyleSheet(f"""
            font-size: 30px;
            font-weight: bold;
            color: {COR_TEXTO};
        """)
        v50.addWidget(self.titulo)
        v50.addStretch()
        self.contador = QLabel("0 itens")
        self.contador.setStyleSheet(estilo_pilula())
        v50.addWidget(self.contador)
        v79.addLayout(v50)
        self.informacao_almoco = QLabel()
        self.informacao_almoco.setWordWrap(True)
        self.informacao_almoco.setStyleSheet(f"""
            QLabel {{
                background: {COR_SUPERFICIE};
                border: 1px solid {COR_BORDA};
                border-radius: 10px;
                padding: 10px 14px;
                color: {COR_TEXTO_SUAVE};
                font-size: 13px;
            }}
        """)
        v79.addWidget(self.informacao_almoco)
        v80 = QScrollArea()
        v80.setWidgetResizable(True)
        v80.setFrameShape(QFrame.NoFrame)
        v80.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.area_produtos = QWidget()
        self.grid = QGridLayout(self.area_produtos)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(16)
        self.grid.setVerticalSpacing(16)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        v80.setWidget(self.area_produtos)
        v79.addWidget(v80)
        v73.addWidget(v78, 1)
        return v69
    def criar_botao_categoria(self, v26, v8, v81):
        v82 = QPushButton(v8)
        v82.setFixedHeight(46)
        v82.setCheckable(True)
        v82.setCursor(Qt.PointingHandCursor)
        v82.clicked.connect(lambda: self.mostrar_produtos(v81))
        v82.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid transparent;
                border-radius: 10px;
                color: {COR_TEXTO_SUAVE};
                font-size: 14px;
                font-weight: 600;
                text-align: left;
                padding: 0 14px;
            }}
            QPushButton:hover {{
                background: {COR_SUPERFICIE_2};
                color: {COR_TEXTO};
            }}
            QPushButton:checked {{
                background: {COR_VERDE_TINT};
                border: 1px solid {COR_VERDE_ESCURO};
                color: {COR_VERDE_CLARO};
            }}
        """)
        self.botoes_categoria[v81] = v82
        v26.addWidget(v82)
    def obter_dia(self):
        v83 = {
            0: "segunda",
            1: "terca",
            2: "quarta",
            3: "quinta",
            4: "sexta",
            5: "sabado",
            6: "domingo"
        }
        return v83[datetime.now().weekday()]
    def limpar_grid(self):
        while self.grid.count():
            v54 = self.grid.takeAt(0)
            if v54.widget():
                v54.widget().deleteLater()
    def mostrar_produtos(self, v81):
        self.titulo.setText(v81)
        for v140, v141 in getattr(self, "botoes_categoria", {}).items():
            v141.setChecked(v140 == v81)
        self.limpar_grid()
        for v84 in range(v4):
            self.grid.setColumnStretch(v84, 0)
            self.grid.setColumnMinimumWidth(v84, 0)
        v85 = self.produtos.get(v81, [])
        self.informacao_almoco.setText(
            f"<b>{v81}</b> • "
            "Escolha um produto para adicionar ao pedido."
        )
        if not v85:
            v134 = QLabel("Nenhum produto disponível nesta categoria.")
            v134.setAlignment(Qt.AlignCenter)
            v134.setStyleSheet(
                f"font-size: 16px; color: {COR_TEXTO_SUAVE}; padding: 40px;"
            )
            self.grid.addWidget(v134, 0, 0)
            return
        v86 = min(v4, max(1, len(v85)))
        for v87 in range(v86):
            self.grid.setColumnStretch(v87, 1)
        for v135, v24 in enumerate(v85):
            v136 = CardProduto(v24, self.adicionar)
            self.grid.addWidget(v136, v135 // v86, v135 % v86)
        for v87 in range(v86):
            self.grid.setColumnMinimumWidth(v87, 1)
    def formatar_previa(self, v88, v64):
        v89 = "item" if v88 == 1 else "itens"
        return (
            f"<span style='font-size: 11px; font-weight: bold; "
            f"color: {COR_TEXTO_FRACO};'>SEU PEDIDO</span><br>"
            f"<span style='font-size: 13px; color: {COR_TEXTO_SUAVE};'>"
            f"{v88} {v89}</span><br>"
            f"<span style='font-size: 20px; font-weight: bold; "
            f"color: {COR_VERDE_CLARO};'>{formatar_moeda(v64)}</span>"
        )
    def atualizar_previa_carrinho(self):
        if not hasattr(self, "previa_carrinho"):
            return
        v88 = sum(v54["quantidade"] for v54 in self.carrinho)
        v64 = sum(
            v54["produto"]["preco"] * v54["quantidade"]
            for v54 in self.carrinho
        )
        self.previa_carrinho.setText(self.formatar_previa(v88, v64))
    def adicionar(self, v24):
        for v54 in self.carrinho:
            if v54["produto"]["nome"] == v24["nome"]:
                v54["quantidade"] += 1
                self.atualizar_contador()
                self.atualizar_previa_carrinho()
                return
        self.carrinho.append({
            "produto": v24,
            "quantidade": 1
        })
        self.atualizar_contador()
        self.atualizar_previa_carrinho()
    def atualizar_contador(self):
        v88 = sum(v54["quantidade"] for v54 in self.carrinho)
        v89 = "item" if v88 == 1 else "itens"
        self.contador.setText(f"{v88} {v89}")
    def abrir_carrinho(self):
        self.pagina_carrinho.definir_itens(self.carrinho)
        self.stack.setCurrentWidget(self.pagina_carrinho)
    def voltar_para_menu(self):
        self.atualizar_contador()
        self.atualizar_previa_carrinho()
        self.stack.setCurrentWidget(self.pagina_menu)
    def confirmar_compra(self):
        if not self.carrinho:
            caixa_mensagem(
                self,
                "Carrinho",
                "Adicione pelo menos um produto."
            )
            return
        v10, v137 = self.criar_dialogo_nome()
        if not v137:
            return
        v10 = v10.strip()
        if not v10:
            caixa_mensagem(
                self,
                "Nome obrigatório",
                "Digite o nome do comprador."
            )
            return
        v64 = self.pagina_carrinho.obter_total()
        v68 = caixa_mensagem(
            self,
            "Confirmar compra",
            f"Comprador: {v10}\n"
            f"Total: {formatar_moeda(v64)}\n\n"
            "Tem certeza que deseja confirmar a compra?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if v68 != QMessageBox.Yes:
            return
        v90 = self.proximo_numero_comanda()
        v91 = self.gerar_pdf(v10, v90)
        v92 = datetime.now()
        v12 = {
            "id": f"{v92.strftime('%Y%m%d')}_{v90:04d}",
            "numero": v90,
            "nome": v10,
            "criada_em": v92.isoformat(),
            "timestamp": v92.timestamp(),
            "total": v64,
            "itens": [
                {
                    "nome": v54["produto"]["nome"],
                    "quantidade": v54["quantidade"],
                    "preco": v54["produto"]["preco"],
                    "imediato": bool(v54["produto"].get("imediato", False)),
                }
                for v54 in self.carrinho
            ],
        }
        salvar_comanda_pendente(v12)
        caixa_mensagem(
            self,
            "Compra concluída",
            "Compra confirmada!\n\n"
            f"Comanda gerada em:\n{v91}"
        )
        self.carrinho.clear()
        self.pagina_carrinho.definir_itens(self.carrinho)
        self.atualizar_contador()
        self.atualizar_previa_carrinho()
        self.abrir_pdf(v91)
        self.stack.setCurrentWidget(self.pagina_boas_vindas)
    def criar_dialogo_nome(self):
        v10, v137 = pedir_texto(
            self,
            "Identificação",
            "Digite o nome do comprador:"
        )
        return v10, v137
    def proximo_numero_comanda(self):
        v93 = datetime.now().strftime("%Y-%m-%d")
        try:
            if self.arquivo_contador.exists():
                v22 = json.loads(
                    self.arquivo_contador.read_text(encoding="utf-8")
                )
            else:
                v22 = {}
        except Exception:
            v22 = {}
        if v22.get("data") != v93:
            v51 = 1
        else:
            v51 = int(v22.get("numero", 0)) + 1
        v22 = {
            "data": v93,
            "numero": v51
        }
        self.arquivo_contador.write_text(
            json.dumps(v22, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return v51
    def gerar_pdf(self, v10, v90):
        v3.mkdir(exist_ok=True)
        agora = datetime.now()
        numero = int(v90)
        arquivo = v3 / f"comanda_{agora.strftime('%Y%m%d')}_{numero:04d}.pdf"
        largura, altura = A4
        doc = canvas.Canvas(str(arquivo), pagesize=A4)
        margem = 18 * mm
        verde = colors.HexColor("#15803d")
        verde_claro = colors.HexColor("#f0fdf4")
        cinza = colors.HexColor("#64748b")
        doc.setFillColor(verde)
        doc.roundRect(margem, altura - 58 * mm, largura - 2 * margem, 40 * mm, 5 * mm, fill=1, stroke=0)
        doc.setFillColor(colors.white)
        doc.setFont("Helvetica-Bold", 23)
        doc.drawString(margem + 8 * mm, altura - 32 * mm, "Cantina do Pablo")
        doc.setFont("Helvetica", 10)
        doc.drawString(margem + 8 * mm, altura - 39 * mm, "Comprovante de pedido")
        doc.setFont("Helvetica-Bold", 24)
        doc.drawRightString(largura - margem - 8 * mm, altura - 34 * mm, f"#{numero:04d}")
        y = altura - 70 * mm
        doc.setFillColor(cinza)
        doc.setFont("Helvetica-Bold", 9)
        doc.drawString(margem, y, "CLIENTE")
        doc.drawString(margem, y - 6 * mm, "DATA E HORA")
        doc.setFillColor(colors.HexColor("#111827"))
        doc.setFont("Helvetica-Bold", 12)
        doc.drawString(margem + 28 * mm, y, v10[:45])
        doc.setFont("Helvetica", 11)
        doc.drawString(margem + 28 * mm, y - 6 * mm, agora.strftime("%d/%m/%Y às %H:%M"))
        y -= 17 * mm
        x1 = margem
        x2 = margem + 18 * mm
        x3 = margem + 105 * mm
        x4 = largura - margem - 34 * mm
        x5 = largura - margem
        doc.setFillColor(verde)
        doc.roundRect(x1, y - 9 * mm, x5 - x1, 9 * mm, 2 * mm, fill=1, stroke=0)
        doc.setFillColor(colors.white)
        doc.setFont("Helvetica-Bold", 9)
        doc.drawString(x1 + 4 * mm, y - 6 * mm, "QTD.")
        doc.drawString(x2 + 3 * mm, y - 6 * mm, "PRODUTO")
        doc.drawRightString(x4 - 3 * mm, y - 6 * mm, "UNIT.")
        doc.drawRightString(x5 - 3 * mm, y - 6 * mm, "TOTAL")
        y -= 10 * mm
        total = 0
        for item in self.carrinho:
            produto = item["produto"]
            qtd = item["quantidade"]
            unit = produto["preco"]
            subtotal = qtd * unit
            total += subtotal
            doc.setFillColor(verde_claro if int((y / mm)) % 2 else colors.white)
            doc.rect(x1, y - 8 * mm, x5 - x1, 8 * mm, fill=1, stroke=0)
            doc.setFillColor(colors.HexColor("#111827"))
            doc.setFont("Helvetica-Bold", 9)
            doc.drawCentredString((x1 + x2) / 2, y - 5 * mm, str(qtd))
            doc.setFont("Helvetica", 9)
            doc.drawString(x2 + 3 * mm, y - 5 * mm, produto["nome"][:42])
            doc.drawRightString(x4 - 3 * mm, y - 5 * mm, f"R$ {unit:.2f}".replace(".", ","))
            doc.drawRightString(x5 - 3 * mm, y - 5 * mm, f"R$ {subtotal:.2f}".replace(".", ","))
            y -= 8 * mm
            if y < 55 * mm:
                doc.showPage()
                y = altura - 25 * mm
        y -= 10 * mm
        doc.setFillColor(colors.HexColor("#f0fdf4"))
        doc.roundRect(x1, y - 25 * mm, x5 - x1, 25 * mm, 4 * mm, fill=1, stroke=0)
        doc.setFillColor(verde)
        doc.setFont("Helvetica-Bold", 11)
        doc.drawString(x1 + 7 * mm, y - 10 * mm, "VALOR TOTAL")
        doc.setFont("Helvetica-Bold", 20)
        doc.drawRightString(x5 - 7 * mm, y - 12 * mm, f"R$ {total:.2f}".replace(".", ","))
        doc.setFillColor(cinza)
        doc.setFont("Helvetica", 8)
        doc.drawCentredString(largura / 2, 16 * mm, "Obrigado pela preferência • Cantina do Pablo")
        doc.save()
        return arquivo
    def abrir_pdf(self, v39):
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(v39)))
        except Exception:
            pass
class JanelaAdmin(QWidget):
    COLUNAS = 4
    """Painel do administrador: comandas pendentes divididas em
    Imediatos (topo) e Não imediatos (base), em grade, ordenadas
    por ordem de chegada."""
    v14 = 4
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painel do Administrador - Cantina do Pablo")
        self.setObjectName("janela")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.resize(1400, 900)
        self.setMinimumSize(1000, 700)
        v26 = QVBoxLayout(self)
        v26.setContentsMargins(28, 24, 28, 24)
        v26.setSpacing(18)
        v50 = QHBoxLayout()
        v50.setSpacing(14)
        v51 = QLabel("P")
        v51.setFixedSize(46, 46)
        v51.setAlignment(Qt.AlignCenter)
        v51.setStyleSheet(estilo_marca(24, 12))
        v50.addWidget(v51)
        v52 = QVBoxLayout()
        v52.setSpacing(2)
        v60 = QLabel("Painel de Comandas")
        v60.setStyleSheet(
            f"font-size: 26px; font-weight: bold; color: {COR_TEXTO}; "
            "background: transparent;"
        )
        v52.addWidget(v60)
        v53 = QLabel("Acompanhe os pedidos pendentes. A lista atualiza sozinha.")
        v53.setStyleSheet(
            f"font-size: 13px; color: {COR_TEXTO_SUAVE}; background: transparent;"
        )
        v52.addWidget(v53)
        v50.addLayout(v52)
        v50.addStretch()
        self.contador = QLabel()
        self.contador.setStyleSheet(estilo_pilula(COR_VERDE_CLARO))
        v50.addWidget(self.contador)
        v108 = QPushButton("Atualizar")
        v108.setFixedSize(120, 42)
        v108.setCursor(Qt.PointingHandCursor)
        v108.clicked.connect(self.atualizar)
        v108.setStyleSheet(estilo_btn_secundario(14, 10))
        v50.addWidget(v108)
        v109 = QPushButton("Produtos")
        v109.setFixedSize(120, 42)
        v109.setCursor(Qt.PointingHandCursor)
        v109.clicked.connect(self.abrir_produtos)
        v109.setStyleSheet(estilo_btn_primario(14, 10))
        v50.addWidget(v109)
        v26.addLayout(v50)
        v80 = QScrollArea()
        v80.setWidgetResizable(True)
        v80.setFrameShape(QFrame.NoFrame)
        self.conteudo = QWidget()
        self.conteudo_layout = QVBoxLayout(self.conteudo)
        self.conteudo_layout.setContentsMargins(0, 0, 0, 0)
        self.conteudo_layout.setSpacing(20)
        self.secao_imediatos = self._criar_secao(
            "Imediatos",
            "Pratos feitos, espetos, mistos e pão com ovo",
            COR_VERDE
        )
        self.conteudo_layout.addWidget(self.secao_imediatos["widget"])
        self.secao_nao_imediatos = self._criar_secao(
            "Não imediatos",
            "Demais itens (bebidas, doces, salgados frios…)",
            COR_TEXTO_FRACO
        )
        self.conteudo_layout.addWidget(self.secao_nao_imediatos["widget"])
        self.conteudo_layout.addStretch()
        v80.setWidget(self.conteudo)
        v26.addWidget(v80)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar)
        self.timer.start(4000)
        self.atualizar()
    def abrir_produtos(self):
        self.produtos_janela = JanelaProdutos()
        self.produtos_janela.show()
    def _criar_secao(self, v60, v71, v109):
        v110 = QFrame()
        v110.setObjectName("secao")
        v110.setStyleSheet(f"""
            QFrame#secao {{
                background: {COR_SUPERFICIE};
                border: 1px solid {COR_BORDA};
                border-radius: 16px;
            }}
        """)
        v111 = QVBoxLayout(v110)
        v111.setContentsMargins(20, 16, 20, 20)
        v111.setSpacing(14)
        v112 = QHBoxLayout()
        v112.setSpacing(10)
        v119 = QLabel()
        v119.setFixedSize(10, 10)
        v119.setStyleSheet(
            f"background: {v109}; border-radius: 5px; border: none;"
        )
        v112.addWidget(v119, alignment=Qt.AlignVCenter)
        v113 = QLabel(v60)
        v113.setStyleSheet(
            f"font-size: 19px; font-weight: bold; color: {COR_TEXTO}; "
            "background: transparent; border: none;"
        )
        v112.addWidget(v113)
        v112.addSpacing(6)
        v114 = QLabel(v71)
        v114.setStyleSheet(
            f"font-size: 12px; color: {COR_TEXTO_FRACO}; "
            "background: transparent; border: none;"
        )
        v112.addWidget(v114)
        v112.addStretch()
        v115 = QLabel("0 comandas")
        v115.setStyleSheet(estilo_pilula())
        v112.addWidget(v115)
        v111.addLayout(v112)
        v116 = QWidget()
        v116.setStyleSheet("background: transparent; border: none;")
        v117 = QGridLayout(v116)
        v117.setContentsMargins(0, 0, 0, 0)
        v117.setHorizontalSpacing(14)
        v117.setVerticalSpacing(14)
        v117.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        v111.addWidget(v116)
        v118 = QLabel("Nenhuma comanda pendente nesta categoria.")
        v118.setAlignment(Qt.AlignCenter)
        v118.setStyleSheet(
            f"font-size: 14px; color: {COR_TEXTO_FRACO}; padding: 34px; "
            "background: transparent; border: none;"
        )
        v111.addWidget(v118)
        return {
            "widget": v110,
            "grid": v117,
            "vazio": v118,
            "contador": v115,
        }
    def _limpar_grid(self, v117):
        while v117.count():
            v54 = v117.takeAt(0)
            if v54.widget():
                v54.widget().deleteLater()
    def _preencher_secao(self, v119, v11):
        v117 = v119["grid"]
        self._limpar_grid(v117)
        if not v11:
            v119["vazio"].setVisible(True)
            v119["contador"].setText("0 comandas")
            return
        v119["vazio"].setVisible(False)
        v120 = len(v11)
        v89 = "comanda" if v120 == 1 else "comandas"
        v119["contador"].setText(f"{v120} {v89}")
        for v135, v12 in enumerate(v11):
            v136 = CardComanda(v12, self.marcar_pronto)
            v117.addWidget(v136, v135 // self.COLUNAS, v135 % self.COLUNAS)
    def marcar_pronto(self, v13):
        v68 = caixa_mensagem(
            self,
            "Confirmar",
            "Marcar esta comanda como pronta e retirá-la do painel?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if v68 != QMessageBox.Yes:
            return
        remover_comanda_pendente(v13)
        self.atualizar()
    def atualizar(self):
        v11 = carregar_comandas_pendentes()
        v121 = [v23 for v23 in v11 if comanda_tem_imediato(v23)]
        v122 = [v23 for v23 in v11 if not comanda_tem_imediato(v23)]
        self._preencher_secao(self.secao_imediatos, v121)
        self._preencher_secao(self.secao_nao_imediatos, v122)
        v64 = len(v11)
        v89 = "comanda" if v64 == 1 else "comandas"
        self.contador.setText(f"{v64} {v89} pendente(s)")

class JanelaProdutos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Produtos - Cantina do Pablo")
        self.setObjectName("janela")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.resize(1050, 700)
        self.setMinimumSize(900, 600)
        self.produtos = self._carregar()
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(28, 24, 28, 24)
        raiz.setSpacing(18)
        topo = QHBoxLayout()
        topo.setSpacing(14)
        bloco = QVBoxLayout()
        bloco.setSpacing(2)
        titulo = QLabel("Cadastro de Produtos")
        titulo.setStyleSheet(
            f"font-size: 26px; font-weight: bold; color: {COR_TEXTO}; "
            "background: transparent;"
        )
        bloco.addWidget(titulo)
        subtitulo = QLabel("Cadastre, edite e remova os produtos exibidos no totem.")
        subtitulo.setStyleSheet(
            f"font-size: 13px; color: {COR_TEXTO_SUAVE}; background: transparent;"
        )
        bloco.addWidget(subtitulo)
        topo.addLayout(bloco)
        topo.addStretch()
        novo = QPushButton("Novo produto")
        novo.setFixedHeight(42)
        novo.setCursor(Qt.PointingHandCursor)
        novo.clicked.connect(self.novo)
        novo.setStyleSheet(self._botao())
        topo.addWidget(novo)
        raiz.addLayout(topo)
        corpo = QHBoxLayout()
        corpo.setSpacing(18)
        self.lista = QListWidget()
        self.lista.setMinimumWidth(360)
        self.lista.currentItemChanged.connect(self.editar_selecionado)
        corpo.addWidget(self.lista)
        painel = QFrame()
        painel.setObjectName("painel_form")
        painel.setStyleSheet(f"""
            QFrame#painel_form {{
                background: {COR_SUPERFICIE};
                border: 1px solid {COR_BORDA};
                border-radius: 16px;
            }}
            QFrame#painel_form QLabel {{
                color: {COR_TEXTO_SUAVE};
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        form = QFormLayout(painel)
        form.setContentsMargins(24, 24, 24, 24)
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome do produto")
        self.desc = QLineEdit()
        self.desc.setPlaceholderText("Descrição")
        self.preco = QDoubleSpinBox()
        self.preco.setRange(0, 99999)
        self.preco.setDecimals(2)
        self.preco.setPrefix("R$ ")
        self.categoria = QComboBox()
        self.imagem = QLineEdit()
        self.imagem.setReadOnly(True)
        escolher = QPushButton("Escolher imagem")
        escolher.setFixedHeight(40)
        escolher.setCursor(Qt.PointingHandCursor)
        escolher.clicked.connect(self.escolher_imagem)
        escolher.setStyleSheet(estilo_btn_secundario(13, 8))
        img_linha = QHBoxLayout()
        img_linha.setSpacing(10)
        img_linha.addWidget(self.imagem)
        img_linha.addWidget(escolher)
        self.previa = QLabel("Sem imagem")
        self.previa.setFixedSize(180, 150)
        self.previa.setAlignment(Qt.AlignCenter)
        self.previa.setStyleSheet(f"""
            QLabel {{
                background: {COR_IMAGEM_FUNDO};
                border: 1px solid {COR_BORDA};
                border-radius: 12px;
                color: {COR_IMAGEM_TEXTO};
                font-size: 13px;
                font-weight: normal;
            }}
        """)
        form.addRow("Nome:", self.nome)
        form.addRow("Descrição:", self.desc)
        form.addRow("Preço:", self.preco)
        form.addRow("Categoria:", self.categoria)
        form.addRow("Imagem:", img_linha)
        form.addRow("", self.previa)
        botoes = QHBoxLayout()
        botoes.setSpacing(10)
        salvar = QPushButton("Salvar")
        salvar.setFixedHeight(42)
        salvar.setCursor(Qt.PointingHandCursor)
        salvar.clicked.connect(self.salvar)
        excluir = QPushButton("Excluir")
        excluir.setFixedHeight(42)
        excluir.setCursor(Qt.PointingHandCursor)
        excluir.clicked.connect(self.excluir)
        salvar.setStyleSheet(self._botao())
        excluir.setStyleSheet(estilo_btn_perigo(14, 10))
        botoes.addWidget(salvar)
        botoes.addWidget(excluir)
        form.addRow("", botoes)
        corpo.addWidget(painel, 1)
        raiz.addLayout(corpo)
        self._atualizar_categorias()
        self._atualizar_lista()

    def _botao(self):
        return estilo_btn_primario(14, 10)

    def _carregar(self):
        return carregar_produtos({})

    def _atualizar_categorias(self):
        atual = self.categoria.currentText()
        self.categoria.clear()
        self.categoria.addItems(list(self.produtos.keys()))
        if atual:
            i = self.categoria.findText(atual)
            if i >= 0:
                self.categoria.setCurrentIndex(i)

    def _atualizar_lista(self):
        self.lista.clear()
        for cat, itens in self.produtos.items():
            for item in itens:
                row = QListWidgetItem(f"{item.get('nome', 'Sem nome')}  •  {cat}")
                row.setData(Qt.UserRole, (cat, item))
                self.lista.addItem(row)

    def escolher_imagem(self):
        arq, _ = QFileDialog.getOpenFileName(self, "Escolher imagem", "", "Imagens (*.png *.jpg *.jpeg *.webp)")
        if not arq:
            return
        origem = Path(arq)
        destino = v2 / origem.name
        if origem.resolve() != destino.resolve():
            shutil.copy2(origem, destino)
        self.imagem.setText(origem.name)
        self._mostrar_imagem(origem.name)

    def _mostrar_imagem(self, nome):
        pix = QPixmap(str(v2 / Path(nome).name))
        if pix.isNull():
            self.previa.setText("Imagem não encontrada")
            self.previa.setPixmap(QPixmap())
        else:
            self.previa.setPixmap(pix.scaled(170, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def editar_selecionado(self, atual, anterior):
        if not atual:
            return
        cat, item = atual.data(Qt.UserRole)
        self.nome.setText(item.get("nome", ""))
        self.desc.setText(item.get("descricao", ""))
        self.preco.setValue(float(item.get("preco", 0) or 0))
        self._atualizar_categorias()
        i = self.categoria.findText(cat)
        if i >= 0:
            self.categoria.setCurrentIndex(i)
        self.imagem.setText(item.get("imagem", ""))
        self._mostrar_imagem(item.get("imagem", ""))

    def novo(self):
        self.lista.clearSelection()
        self.nome.clear()
        self.desc.clear()
        self.preco.setValue(0)
        self.imagem.clear()
        self.previa.setText("Sem imagem")
        self.previa.setPixmap(QPixmap())
        if self.categoria.count():
            self.categoria.setCurrentIndex(0)
        self.nome.setFocus()

    def salvar(self):
        nome = self.nome.text().strip()
        desc = self.desc.text().strip()
        img = self.imagem.text().strip()
        cat = self.categoria.currentText()
        preco = self.preco.value()
        if not nome or not cat or not img:
            caixa_mensagem(self, "Campos obrigatórios", "Informe nome, categoria e imagem.")
            return
        atual = self.lista.currentItem()
        antigo = atual.data(Qt.UserRole) if atual else None
        if antigo:
            oc, oi = antigo
            self.produtos[oc] = [x for x in self.produtos.get(oc, []) if x is not oi]
        novo = {"nome": nome, "descricao": desc, "preco": preco, "imagem": Path(img).name}
        self.produtos.setdefault(cat, []).append(novo)
        salvar_produtos(self.produtos)
        self._atualizar_categorias()
        self._atualizar_lista()
        caixa_mensagem(self, "Produto salvo", "Produto salvo com sucesso. O totem usará os dados atualizados.")

    def excluir(self):
        atual = self.lista.currentItem()
        if not atual:
            return
        cat, item = atual.data(Qt.UserRole)
        if caixa_mensagem(self, "Excluir produto", f"Excluir <b>{item['nome']}</b>?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        self.produtos[cat] = [x for x in self.produtos.get(cat, []) if x is not item]
        if not self.produtos[cat]:
            del self.produtos[cat]
        salvar_produtos(self.produtos)
        self._atualizar_categorias()
        self._atualizar_lista()
        self.novo()

class DialogoSenhaAdmin(QDialog):
    """Tela de acesso administrativo no mesmo estilo visual do projeto."""

    def __init__(self, pai=None):
        super().__init__(pai)
        self.setWindowTitle("Acesso administrativo")
        self.setModal(True)
        self.setMinimumWidth(460)
        self.setObjectName("dialogoSenha")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(14)

        marca = QLabel("P")
        marca.setFixedSize(48, 48)
        marca.setAlignment(Qt.AlignCenter)
        marca.setStyleSheet(estilo_marca(24, 12))
        layout.addWidget(marca, 0, Qt.AlignLeft)

        titulo = QLabel("Acesso administrativo")
        titulo.setStyleSheet(f"""
            QLabel {{
                color: {COR_TEXTO};
                font-size: 22px;
                font-weight: 700;
                background: transparent;
            }}
        """)
        layout.addWidget(titulo)

        subtitulo = QLabel("Digite a senha para abrir o painel de administração.")
        subtitulo.setWordWrap(True)
        subtitulo.setStyleSheet(f"""
            QLabel {{
                color: {COR_TEXTO_SUAVE};
                font-size: 13px;
                background: transparent;
            }}
        """)
        layout.addWidget(subtitulo)

        self.senha = QLineEdit()
        self.senha.setEchoMode(QLineEdit.Password)
        self.senha.setPlaceholderText("Senha do administrador")
        self.senha.setFixedHeight(46)
        self.senha.returnPressed.connect(self.accept)
        layout.addWidget(self.senha)

        botoes = QHBoxLayout()
        botoes.setSpacing(10)
        botoes.addStretch()

        cancelar = QPushButton("Cancelar")
        cancelar.setFixedHeight(42)
        cancelar.setCursor(Qt.PointingHandCursor)
        cancelar.setStyleSheet(estilo_btn_secundario(13, 9))
        cancelar.clicked.connect(self.reject)

        confirmar = QPushButton("Entrar")
        confirmar.setFixedHeight(42)
        confirmar.setMinimumWidth(110)
        confirmar.setCursor(Qt.PointingHandCursor)
        confirmar.setStyleSheet(estilo_btn_primario(13, 9))
        confirmar.clicked.connect(self.accept)

        botoes.addWidget(cancelar)
        botoes.addWidget(confirmar)
        layout.addLayout(botoes)

        self.senha.setFocus()


def pedir_senha_admin(v15=None, v16=3):
    """Solicita a senha do administrador, sem revelar o número de tentativas."""
    for _ in range(v16):
        dialogo = DialogoSenhaAdmin(v15)
        if dialogo.exec() != QDialog.Accepted:
            return False
        if dialogo.senha.text() == v5:
            return True
        caixa_mensagem(
            v15,
            "Senha incorreta",
            "A senha digitada está incorreta. Tente novamente."
        )
    return False
if __name__ == "__main__":
    v18 = QApplication(sys.argv)
    v18.setStyle("Fusion")
    aplicar_paleta_escura(v18)
    v18.setStyleSheet(ESTILO_GLOBAL)
    v19 = Totem()
    v19.show()
    if pedir_senha_admin(v19):
        v123 = JanelaAdmin()
        v123.show()
    else:
        caixa_mensagem(
            v19,
            "Acesso negado",
            "O painel do administrador não será aberto."
        )
    sys.exit(v18.exec())
