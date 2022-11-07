import logging
from parser import base_currencies, client

from PyQt6 import QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.log = lambda *args_, **kwargs_: logging.log(logging.DEBUG + 5, *args_, **kwargs_)

        # Main window
        self.setWindowTitle("Crypto-predictor")

        # Central widget
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Currencies
        self.currencies_group = QtWidgets.QGroupBox()
        self.central_widget_layout.addWidget(self.currencies_group)
        self.currencies_layout = QtWidgets.QHBoxLayout(self.currencies_group)
        self.currencies_group.setStyleSheet("QComboBox { combobox-popup: 0; }")
        # Crypto currency combobox
        self.crypto_currency = QtWidgets.QComboBox()
        self.crypto_currency.setMaxVisibleItems(20)
        self.crypto_currency.currentTextChanged.connect(self._change_crypto_currency_combobox_event)
        self.crypto_currency_block = True
        self.crypto_currency.installEventFilter(self.crypto_currency)
        self.crypto_currency_current: str = "BTC"
        self.currencies_layout.addWidget(self.crypto_currency)
        # '/' label between comboboxes
        label = QtWidgets.QLabel(" / ")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        )
        self.currencies_layout.addWidget(label)
        # Base currency combobox
        self.base_currency = QtWidgets.QComboBox()
        self.base_currency.setMaxVisibleItems(20)
        self.base_currency.currentTextChanged.connect(self._change_base_currency_combobox_event)
        self.base_currency_block = True
        self.base_currency_current: str = "USD"
        self.currencies_layout.addWidget(self.base_currency)

        # Graph (stub)
        self.graph_widget = QtWidgets.QLabel()
        self.central_widget_layout.addWidget(self.graph_widget)
        self.graph_widget.setStyleSheet("QLabel { background-color: #222; }")

        # Control panel
        self.control_group = QtWidgets.QGroupBox()
        self.central_widget_layout.addWidget(self.control_group)
        self.control_group_layout = QtWidgets.QHBoxLayout(self.control_group)
        self.control_checkbox_run = QtWidgets.QCheckBox()
        self.control_group_layout.addWidget(self.control_checkbox_run)
        self.control_checkbox_run.clicked.connect(self._control_checkbox_run_event)
        self.control_checkbox_run.setText("Run")
        self.control_checkbox_learn = QtWidgets.QCheckBox()
        self.control_group_layout.addWidget(self.control_checkbox_learn)
        self.control_checkbox_learn.setText("Learn")
        self.control_checkbox_predicate = QtWidgets.QCheckBox()
        self.control_group_layout.addWidget(self.control_checkbox_predicate)
        self.control_checkbox_predicate.setText("Predicate")

        # Final logic
        self._fill_currency_combobox()

    def _fill_currency_combobox(self) -> None:
        self.log("self._fill_currency_combobox()")
        for currency in base_currencies:
            self.base_currency.addItem(currency["id"])
        self.base_currency_block = False
        self.base_currency.setCurrentText(self.base_currency_current)

    def _change_base_currency_combobox_event(self, base_currency_str) -> None:
        if self.base_currency_block:
            return
        self.log(f"self._change_base_currency_combobox_event({base_currency_str=})")
        self.crypto_currency_block = True
        self.rates = client.get_exchange_rates(currency=base_currency_str)["rates"]
        for rate in self.rates:
            self.crypto_currency.addItem(rate)
        self.crypto_currency.setCurrentText(self.crypto_currency_current)
        self._change_crypto_currency_combobox()
        self.crypto_currency_block = False

    def _change_crypto_currency_combobox_event(self, crypto_currency_str) -> None:
        if self.crypto_currency_block:
            return
        self.crypto_currency_current = crypto_currency_str
        self.log(f"self._change_crypto_currency_combobox_event({crypto_currency_str=})")
        self._change_crypto_currency_combobox()

    def _change_crypto_currency_combobox(self) -> None:
        self.log("self._change_crypto_currency_combobox()")
        price = self.rates[self.crypto_currency_current]
        self.graph_widget.setText(price)

    def _control_checkbox_run_event(self, b: bool) -> None:
        self.currencies_group.setEnabled(not b)
